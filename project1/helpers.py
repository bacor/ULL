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

def add_word_boundaries4(corpus, boundaries, sep="."):
    return ''.join((sep+c if b == 1 else c for c, b in zip(corpus, boundaries)))

def add_word_boundaries(corpus, boundaries, sep="."):
    boundaries = iter(sorted(boundaries))
    cur_b = boundaries.__next__()
    out = ""

    for i in range(len(corpus)):
        if cur_b == i:
            if not corpus[i] == "$":
                out += sep
            try:
                cur_b = boundaries.__next__()
            except StopIteration:
                out += corpus[i:]
                break
        out += corpus[i]
    return out

def add_word_boundaries3(corpus, boundaries, sep="."):
    return ''.join([sep+corpus[i] if i in boundaries and corpus[i] != "$"
                                else corpus[i] for i in range(len(corpus))])

def add_word_boundaries2(corpus, boundaries, sep="."):
    """Adds word boundaries to a corpus by inserting a sepator at every boundary
    """
    out = ""
    prev_b = 0
    for b in boundaries:
        out += corpus[prev_b:b] + sep
        prev_b = b
    return out

def get_words_counts(corpus, boundaries):
    """Counts all words in a corpus given the word boundaries"""
    counts = Counter()
    prev_b = boundaries[0] # always equals 0
    for b in boundaries[1:]:
        word = corpus[prev_b:b]
        counts[word] += 1
        prev_b = b
    return counts    

def read_data(filename):
    pattern = re.compile('\s+')
    result_ls = []
    with open(filename) as handle:
        for line in handle:
            line = re.sub(pattern, '', line)
            result_ls.append(line)
    return result_ls