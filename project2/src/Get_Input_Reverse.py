import re
import numpy as np

from Story import Story, Question, Statement


##### input ######
# for the answering task:
# assume maximum length of vectors: l
# get number of words in vocabulary: v
# number of sentences input: n
# for each story: n x l x v tensor

# for the reversing task:
# get maximum sentence length: l
# get number of words in vocabulary: v
# for each sentence: l x v matrix


# in dimension v: one-hot vectors



# corpus file formats:
# ID statement
# ID statement
# ID statement
# ID question [TAB] answer [TAB] 'IDs of supporting fact'
def read_corpus_file(filename):
    with open(filename) as handle:
        for line in handle:
            yield line


def process_corpus(filename):
    corpus = read_corpus_file(filename,)
    #question_pattern = re.compile('(\d+) (.+\?) ?\t(.+|.+,.+)\t(\d+|\d+\s\d+|\d+\s\d+\s\d+|\d+\s\d+\s\d+\s\d+|\d+\s\d+\s\d+\s\d+\s\d+|\d+\s\d+\s\d+\s\d+\s\d+\s\d+|\d+\s\d+\s\d+\s\d+\s\d+\s\d+\s\d+)\n')
    question_pattern = re.compile('(\d+) (.+\?) ?\t(.+)\t(.+)\n')
    pattern2 = re.compile('(\d+) (.+\?)\t')
    group_range = (1, 5)
    story_ls = []

    for line in corpus:
        match_obj = question_pattern.match(line)
        if match_obj:
            groups = [match_obj.group(i) for i in range(*group_range)]
            dig = groups[3].split(' ')
            i = 0
            while i < len(dig):
                dig[i] = int(dig[i].strip('\n'))
                i += 1
            question_contents = int(groups[0]), groups[1], groups[2], dig
            q = Question(*question_contents)
            #print(q.answer_id)
            story_ls.append(q)
        else:
            id_len = line.index(' ')
            statement_contents = int(line[:id_len]), line[id_len + 1:-1]
            s = Statement(*statement_contents)
            if statement_contents[0] == 1 and not story_ls == []:
                yield Story(story_ls)
                story_ls = []
            story_ls.append(s)
    yield Story(story_ls)


# prepares a corpus for input into
# an ANN by turning its texts into arrays
# of one-hot vectors
# rtype: tuple of:
#  - list of sentences transformed into arrays of one-hot vectors
#  - Dict[str, int] with the index given to each word in the vocabulary
def corpus_to_vecs(corpus):
    corpus = list(corpus)
    vocab_indices = vocab_to_indices(corpus)
    return list(get_text_mats(corpus, vocab_indices)), vocab_indices


# turns the texts in a corpus (a list of Story objects)
# into list of one-hot vectors
# rtype: generator over
# numpy arrays of dim len(sentence) x V
def get_text_mats(corpus, vocab_inds):
    for story in corpus:
        for text in story:
            text_mat = np.asarray(list(text_to_mat(text, vocab_inds)))
            yield text_mat


# turns each word of a text into one-hot vectors
# rtype: generator over vectors with base type int
def text_to_mat(text, vocab_inds):
    vocab_size = len(vocab_inds)

    for word in text:
        yield [1 if vocab_inds[word] == i else 0 for i in range(vocab_size)]


# assigns each word in the corpus and index
# rtype: Dict[string, int]
def vocab_to_indices(corpus):
    indices = {}
    index = 0
    for story in corpus:
        for text in story:
            for word in text:
                if not word in indices:
                    indices[word] = index
                    index += 1
    return indices


def reversed_corpus(text_mats):
    for mat in text_mats:
        yield mat[::-1]

