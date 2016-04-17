###
# Some helper functions

import re
from collections import Counter

def clean_corpus(corpus, sep="$"):
    """Removes utterance boundaries and returns clean corpus
    with utterance boundary positions. The i-th boundary position
    always **preceeds** the i-th character. An initial and final
    boundary are always included

    Args:
        C: a very long string separated by utterance boundaries
        sep: the utterance boundary character, defaults to "$"

    Returns:
        new_C: clean corpus
        U: List with utterance boundary positions
    """

    # Utterance boundary positions
    U = [i for i, w in enumerate(corpus) if w == sep]

    # Remove separators ($) and fix indices in U accordingly
    new_corpus = corpus.replace(sep, "")
    U = [U[i] - i for i in range(len(U))]
    U += [0, len(new_corpus)]

    return new_corpus, sorted(set(U))

# operates on binary list
def add_word_boundaries(corpus, boundaries, sep="."):
    return ''.join((sep+c if b == 1 else c for c, b in zip(corpus, boundaries)))

def get_words_counts(corpus, boundaries):
    """Counts all words in a corpus given the word boundaries"""
    counts = Counter()
    cur_w = ""
    for i in range(1, len(boundaries)):
        cur_w += corpus[i-1]
        if boundaries[i] == 1:
            counts[cur_w] += 1
            cur_w = ""
    return counts    

def read_data(filename):
    pattern = re.compile('\s+')
    result_ls = []
    with open(filename) as handle:
        for line in handle:
            line = re.sub(pattern, '', line)
            result_ls.append(line)
    return result_ls