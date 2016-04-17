

import numpy as np

import random

import math

from collections import Counter


##### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #####

# Initialise before each sampling step (or in intervals).
# Use the number of word boundaries inferred in the last sampling step
# as an empirical distribution. Given the length of the utterance, what
# is the empirical, expected number of word boundaries?

##### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #####

# initialises the word boundaries based on a Poisson distribution, i.e.
# a number of word boundaries in the utterance is taken
# from a uniform distribution and then this many indices are randomly drawn
def initialise_poisson(data, word_length_factor):
    accum_start_index = 1
    for line in data:
        num_boundaries = np.random.poisson(len(line)/word_length_factor)
        num_boundaries = math.floor(max(0, min(len(line)-1, num_boundaries)))
        boundary_indices = random.sample(range(accum_start_index, accum_start_index+len(line)-1), num_boundaries)
        accum_start_index += len(line)
        for i in boundary_indices:
            yield i
    yield accum_start_index


# initialises the word boundaries completely randomly, i.e. a number of word
# boundaries in the utterance is taken from a uniform distribution and then
# this many indices are randomly drawn
def initialise_random(data):
    accum_start_index = 1
    for line in data:
        num_boundaries = random.randint(0, len(line)-1)
        boundary_indices = random.sample(range(accum_start_index, accum_start_index+len(line)-1), num_boundaries)
        accum_start_index += len(line)
        for i in boundary_indices:
            yield i

# randomly generate word boundary with probability inversely proportional to bigram probability of
# the two surrounding phonemes, i.e. the lower p(phon2|phon1), the higher the probability of a word boundary


def prod(ls):
    p = 1
    for element in ls:
        p *= element
    return p


# empirical distribution of the phonemes
# in terms of bigram sequences
def gather_bigram_phon_probs(data, boundary_prob):

    unigram_probs = gather_unigram_phon_probs(data, boundary_prob)

    bigrams = ((line[i-1], line[i]) if i > 0 else ('$', line[i]) for line in data for i in range(len(line)))

    bigram_probs = Counter(bigrams)
    norm_counter(bigram_probs)

    def phoneme_prob(phon_bigram):
        if phon_bigram[0] == '$':
            return unigram_probs(phon_bigram[1])
        else:
            if bigram_probs[phon_bigram] == 0:
                return unigram_probs(phon_bigram[1])
            else:
                return bigram_probs[phon_bigram]

    def bigram_seq_prob(seq):
        seq_bigrams = ((seq[i-1], seq[i]) if i > 0 else ('$', seq[0]) for i in range(len(seq)))
        p = prod((phoneme_prob(bigram) for bigram in seq_bigrams))

        p *= boundary_prob*(1-boundary_prob)**(len(seq)-1)
        return p

    return bigram_seq_prob


# empirical distribution of the phonemes
# in terms of bigram sequences
def gather_unigram_phon_probs(data, boundary_prob):
    unigram_probs = Counter((phon for line in data for phon in line))
    norm_counter(unigram_probs)

    def unigram_seq_prob(seq):
        p = prod((unigram_probs[phon] for phon in seq))
        p *= boundary_prob*(1-boundary_prob)**(len(seq)-1)
        return p
    return unigram_seq_prob


# each phoneme has the same probability: 1/#(different phonemes)
def gather_uniform_phon_probs(data, boundary_prob):
    single_phons = set((phon for line in data for phon in line))

    def uniform_seq_prob(seq):
        p = boundary_prob*(1-boundary_prob)**(len(seq)-1)
        return p*(1/len(single_phons))**len(seq)

    return uniform_seq_prob


# transforms the counts into probabilities
def norm_counter(counter):
    total = sum(counter.values())
    for key in counter:
        counter[key] /= total