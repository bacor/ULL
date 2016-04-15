from helpers import *
from model2 import *
from Initialisation import *

import cProfile
from collections import Counter


def main_prog():
    
    #### 
    ## A silly demo

    # Get corpus and utterance boundaries
    orig_corpus = "helloworld$hereisanicestory$helloworldnostorypleaseworld"

    # The model is a class now!
    W = WordSegmenter(orig_corpus)
    B = W.initialize([5, 10, 12, 17, 25, 31, 36, 49])

    # orig_corpus = ["ait", "itis"]

    orig_corpus = read_data('data\\br-phono-test.txt')

    total_len = sum(len(ls) for ls in orig_corpus)

    print('TOTAL LENGTH:', total_len)

    orig_corpus = orig_corpus[:]

    # # computes the probabilities of all phonemes and returns a function
    # # which computes the probability of a sequence based on these probabilities
    uni_prob = gather_bigram_phon_probs(orig_corpus, 0.5)


    # # randomly generates word boundaries
    B = list(initialise_poisson(orig_corpus, 5))

    # shallow copy of B to avoid side effects
    B_copy = B[:]

    # # prepare data for WordSegmenter
    orig_corpus = '$'.join((line for line in orig_corpus))


    W = WordSegmenter(orig_corpus)
    B = W.initialize(B)

    print('B', B)

    P0, alpha, rho = lambda w: 1, 50, 0.5
    num_iter = 3

    B = W.sample(B, num_iter, uni_prob, alpha, rho)

    B = [i for i in range(len(B)) if B[i] == 1]

    print('------------')

    print(add_word_boundaries(orig_corpus, B_copy))

    print('------------')

    print(add_word_boundaries(orig_corpus, B))


if __name__ == '__main__':
    main_prog()

    # import cProfile
    #
    # import time
    #
    # start_time = time.time()
    #
    # end_time = time.time() - start_time
    #
    # print('TIME ELAPSED:', end_time)