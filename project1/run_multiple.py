
from model2 import *
import os


if __name__ == '__main__':

    file_name = "data" + os.path.sep + "br-phono-train.txt"

    # first training
    avg_word_len, bound_prob, phon_prob = 3, 0.5, 'uniform'
    # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
    num_iter = 10000
    # fixed - paper says they're the best parameters
    alpha, rho = 50, 2

    W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

    print('---- First training ----')

    B = W.sample(num_iter, alpha, rho)

    print('<Final inferred boundaries>: ', B)



    # second training -- is the same as first training (to check convergence)
    avg_word_len, bound_prob, phon_prob = 3, 0.5, 'uniform'
    # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
    num_iter = 10000
    # fixed - paper says they're the best parameters
    alpha, rho = 50, 2

    W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

    print('---- Second training ----')

    B = W.sample(num_iter, alpha, rho)

    print('<Final inferred boundaries>: ', B)


    # third training -- different initial word length
    avg_word_len, bound_prob, phon_prob = 4, 0.5, 'uniform'
    # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
    num_iter = 10000
    # fixed - paper says they're the best parameters
    alpha, rho = 50, 2

    W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

    print('---- Third training ----')

    B = W.sample(num_iter, alpha, rho)

    print('<Final inferred boundaries>: ', B)


    # fourth training -- different initial word length
    avg_word_len, bound_prob, phon_prob = 5, 0.5, 'uniform'
    # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
    num_iter = 10000
    # fixed - paper says they're the best parameters
    alpha, rho = 50, 2

    W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

    print('---- Fourth training ----')

    B = W.sample(num_iter, alpha, rho)

    print('<Final inferred boundaries>: ', B)


    # fifth training -- unigram probs
    avg_word_len, bound_prob, phon_prob = 3, 0.5, 'unigram'
    # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
    num_iter = 10000
    # fixed - paper says they're the best parameters
    alpha, rho = 50, 2

    W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

    print('---- Fifth training ----')

    B = W.sample(num_iter, alpha, rho)

    print('<Final inferred boundaries>: ', B)


    # sixth training -- unigram probs, different word length
    avg_word_len, bound_prob, phon_prob = 4, 0.5, 'unigram'
    # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
    num_iter = 10000
    # fixed - paper says they're the best parameters
    alpha, rho = 50, 2

    W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

    print('---- Sixth training ----')

    B = W.sample(num_iter, alpha, rho)

    print('<Final inferred boundaries>: ', B)


    # seventh training -- bigram probs
    avg_word_len, bound_prob, phon_prob = 3, 0.5, 'bigram'
    # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
    num_iter = 10000
    # fixed - paper says they're the best parameters
    alpha, rho = 50, 2

    W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

    print('---- Seventh training ----')

    B = W.sample(num_iter, alpha, rho)

    print('<Final inferred boundaries>: ', B)


    # eighth training -- bigram probs, different word length
    avg_word_len, bound_prob, phon_prob = 4, 0.5, 'bigram'
    # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
    num_iter = 10000
    # fixed - paper says they're the best parameters
    alpha, rho = 50, 2

    W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

    print('---- Eighth training ----')

    B = W.sample(num_iter, alpha, rho)

    print('<Final inferred boundaries>: ', B)

