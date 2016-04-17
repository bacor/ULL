from helpers import *
from model2 import *
from Initialisation import *

import cProfile

if __name__ == '__main__':
    w_len, bound_prob, phon_prob = 3, 0.5, 'unigram'
    num_iter = 1
    alpha, rho = 50, 2

    W = WordSegmenter('data\\br-phono-train.txt', w_len, bound_prob, phon_prob)

    # pr = cProfile.Profile()
    #
    # pr.enable()

    # cProfile.run('W.sample(num_iter, alpha, rho)')

    B = W.sample(num_iter, alpha, rho)

    # pr.disable()
    #
    # s = io.StringIO()
    # sortby = 'cumulative'
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())


    print('--- Initial Boundaries:')

    print(add_word_boundaries(W.corpus, W.B))

    print('--- Inferred Boundaries:')

    print(add_word_boundaries(W.corpus, B))