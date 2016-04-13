###
# Some helper functions

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

    return new_corpus, sorted(list(set(U)))



def add_word_boundaries(corpus, boundaries, sep="."):
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