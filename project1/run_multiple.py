
from model2 import *
import os


if __name__ == '__main__':
        file_name = "data" + os.path.sep + "br-phono-train.txt"


        # # first training
        # training_no = 1
        # avg_word_len, bound_prob, phon_prob = 3, 0.5, 'uniform'
        # # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
        # num_iter = 10000
        # # fixed - paper says they're the best parameters
        # alpha, rho = 50, 2
        #
        # W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)
        #
        # print('---- First training ----\n')
        #
        # W.sample_call_id += 1
        # B = W.sample(num_iter, alpha, rho)


        # second training -- is the same as first training (to check convergence)
        training_no = 2
        avg_word_len, bound_prob, phon_prob = 3, 0.5, 'uniform'
        # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
        num_iter = 10000
        # fixed - paper says they're the best parameters
        alpha, rho = 50, 2

        W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

        print('---- Second training ----\n')

        W.sample_call_id = training_no
        B = W.sample(num_iter, alpha, rho)


        # third training -- different initial word length
        training_no = 3
        avg_word_len, bound_prob, phon_prob = 4, 0.5, 'uniform'
        # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
        num_iter = 10000
        # fixed - paper says they're the best parameters
        alpha, rho = 50, 2

        W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

        print('---- Third training ----\n')

        W.sample_call_id = training_no
        B = W.sample(num_iter, alpha, rho)


        # fourth training -- different initial word length
        training_no = 4
        avg_word_len, bound_prob, phon_prob = 5, 0.5, 'uniform'
        # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
        num_iter = 10000
        # fixed - paper says they're the best parameters
        alpha, rho = 50, 2

        W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

        print('---- Fourth training ----\n')

        W.sample_call_id = training_no
        B = W.sample(num_iter, alpha, rho)


        # fifth training -- unigram probs
        training_no = 5
        avg_word_len, bound_prob, phon_prob = 3, 0.5, 'unigram'
        # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
        num_iter = 10000
        # fixed - paper says they're the best parameters
        alpha, rho = 50, 2

        W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

        print('---- Fifth training ----\n')

        W.sample_call_id = training_no
        B = W.sample(num_iter, alpha, rho)


        # sixth training -- unigram probs, different word length
        training_no = 6
        avg_word_len, bound_prob, phon_prob = 4, 0.5, 'unigram'
        # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
        num_iter = 10000
        # fixed - paper says they're the best parameters
        alpha, rho = 50, 2

        W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

        print('---- Sixth training ----\n')

        W.sample_call_id = training_no
        B = W.sample(num_iter, alpha, rho)


        # seventh training -- bigram probs
        training_no = 7
        avg_word_len, bound_prob, phon_prob = 3, 0.5, 'bigram'
        # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
        num_iter = 10000
        # fixed - paper says they're the best parameters
        alpha, rho = 50, 2

        W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

        print('---- Seventh training ----\n')

        W.sample_call_id = training_no
        B = W.sample(num_iter, alpha, rho)


        # eighth training -- bigram probs, different word length
        training_no = 8
        avg_word_len, bound_prob, phon_prob = 4, 0.5, 'bigram'
        # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
        num_iter = 10000
        # fixed - paper says they're the best parameters
        alpha, rho = 50, 2

        W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)

        print('---- Eighth training ----\n')

        W.sample_call_id = training_no
        B = W.sample(num_iter, alpha, rho)

