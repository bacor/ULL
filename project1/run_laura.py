from model import *
import os

if __name__ == '__main__':

        # UNIGRAM!
        phon_prob = 'uniform'

        # Settings constant for everyone
        num_iter = 10000
        avg_word_len = 3
        bound_prob = 0.5
        file_name = "data" + os.path.sep + "br-phono-train.txt"
        alpha = 20
        rho = 2

        print('---- First training ----\n')
        training_no = 1
        W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)
        W.sample_call_id = training_no
        B = W.sample(num_iter, alpha, rho)

        print('---- Second training ----\n')
        training_no = 2
        W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob)
        W.sample_call_id = training_no
        B = W.sample(num_iter, alpha, rho)