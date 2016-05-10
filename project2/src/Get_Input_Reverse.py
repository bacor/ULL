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
    corpus = read_corpus_file(filename)
    question_pattern = re.compile('(\d|\d\d) (.+\?) \t(.+)\t(\d|\d\d)')
    group_range = (1, 5)

    story_ls = []

    for line in corpus:
        match_obj = question_pattern.match(line)
        if match_obj:
            groups = [match_obj.group(i) for i in range(*group_range)]
            question_contents = int(groups[0]), groups[1], groups[2], int(groups[3])
            q = Question(*question_contents)
            story_ls.append(q)
        else:
            id_len = line.index(' ')
            statement_contents = int(line[:id_len]), line[id_len+1:-1]
            s = Statement(*statement_contents)
            if statement_contents[0] == 1 and not story_ls == []:
                yield Story(story_ls)
                story_ls = []
            story_ls.append(s)
    yield Story(story_ls)


# turns the texts in a corpus (a list of Story objects)
# into matrices with the same number one-hot vectors
# rtype: generator over
# numpy arrays of dim V x len(sentence)
def corpus_to_mats(corpus):
    corpus = list(corpus)
    vocab_inds = vocab_to_indices(corpus)
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


if __name__ == '__main__':
    # file = 'Data/en/qa1_single-supporting-fact_test.txt'
    #
    # import os
    #
    # data_dir = 'Data/en/'
    #
    # file_exp = re.compile('qa[1-5]_.+_train\.txt')
    #
    # for file in os.listdir(data_dir):
    #     if file_exp.match(file):
    #         print('file:', file)
    #         c = process_corpus(data_dir+file)


    file = 'Data/en/qa1_single-supporting-fact_test.txt'

    c = list(process_corpus(file))

    texts_mats = list(corpus_to_mats(c))

    print(texts_mats[0])

    print(texts_mats[-1])

    print('-----------------')

    reversed_texts_mats = list(reversed_corpus(texts_mats))

    print(reversed_texts_mats[0])

    print(reversed_texts_mats[-1])
