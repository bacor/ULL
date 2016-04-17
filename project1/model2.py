from helpers import *
from Initialisation import *
import os

class WordSegmenter:
    """WordSegmenter class implements the model"""

    def __init__(self, corpus_file, avg_word_length, boundary_prob, phon_prob='uniform', N=-1):
        """Initialize the class

        Args:
            corpus: an uncleaned corpus (raw text with utterance boundaries etc)
        """

        self.corpus = read_data(corpus_file)
        self.corpus = self.corpus[:N]
        # self.corpus = "helloworld$hereisanicestory$helloworldnostorypleaseworld"*10
        # self.corpus = self.corpus.split("$")

        if phon_prob == 'uniform':
            P0 = gather_uniform_phon_probs(self.corpus, boundary_prob)
        elif phon_prob == 'unigram':
            P0 = gather_unigram_phon_probs(self.corpus, boundary_prob)
        elif phon_prob == 'bigram':
            P0 = gather_bigram_phon_probs(self.corpus, boundary_prob)
        else:
            raise ValueError('Phoneme probability measure must be one of: uniform, unigram, bigram.')

        self.P0 = P0
        self.corpus = '$'.join((line for line in self.corpus))
        self.corpus, self.U = clean_corpus(self.corpus)
        
        # B = set([5, 10, 12, 17, 25, 31, 36, 49]) #DEMO
        B = set(initialise_poisson(self.corpus, avg_word_length))
        B |= set(self.U)
        B = [1 if i in B else 0 for i in range(len(self.corpus)+1)]
        self.B = B

        self.sample_call_id = 1

        self.clean_dictionary_freq = 100

    def get_next_bound(self, pos):
            return next(i for i in range(min(pos, len(self.B)-1), len(self.B)) if self.B[i] == 1)

    def get_prev_bound(self, pos):
        return next((i for i in range(pos, -1, -1) if self.B[i] == 1))

    def sample(self, num_iter, alpha, rho):
        """Samples word boundaries from a corpus using Gibbs-sampling.

        Args:
            B: a list of initial boundary positions
            num_iter: number of iterations
            P0: a function that takes a word and returns its probability
            alpha: hyperparameter
            rho: hyperparameter

        Returns:
            A list of boundary positions sampled from the posterior

        """
        import time
        print('     Start sampling')

        prob_dict = {}

        B = self.B
        P0 = self.P0

        start_time = time.time()

        U = self.U
        last_U = U[-1]
        U = set(U)

        corpus = self.corpus

        # Initialize wordcounts
        wordcounts = get_words_counts(corpus, B)
        num_words = sum(wordcounts.values()) - 1

        for t in range(num_iter):

            if (t % 100) == 0:
                file_name = 'results_training_'+str(self.sample_call_id)+'_iteration_'+str(t)+'.txt'
                with open(file_name, 'a+') as h:
                    h.write('<Boundaries at iteration: ')
                    h.write(str(t))
                    h.write('>: ')
                    h.write(str(B))
                    h.write('\n')

            # Remove first word and (occasionally) all nonpositive ones
            wordcounts[corpus[:self.get_next_bound(1)]] -= 1
            if (t % self.clean_dictionary_freq) == 0:
                wordcounts += Counter()
            
            b_prev_index = 0
            b_prev = 0
            for b_cur in range(1,len(corpus)+1):

                # Is b_cur on the boundary?
                cur_is_on_boundary = (B[b_cur] == 1)

                # Previous and next boundaries
                # b_prev = self.get_prev_bound(b_cur)
                b_next = self.get_next_bound(b_cur + int(cur_is_on_boundary))

                t2 = time.time()
                # Words/fragments in the focus area
                w1 = corpus[b_prev:b_next]
                w2 = corpus[b_prev:b_cur]
                w3 = corpus[b_cur:b_next]

                # Update wordcounts and #words in context
                # wordcounts[w3] -= int(cur_is_on_boundary)
                if cur_is_on_boundary:
                    wordcounts[w3] = max(0, wordcounts[w3] - 1)
                    num_words -= int((len(B)-1 != b_cur))

                # DEBUGGIN of a SMALL corpus!
                # This prints the corpus with word boundaries and wordcounts
                # out = ""
                # for i, char in enumerate(corpus):
                #     if i == b_cur:   out += " | "
                #     elif B[i] == 1:  out += "."
                #     out += char
                # out += "."
                # context = ["%s(%s)" % (w,i) for w, i in wordcounts.items() if i>0]
                # posstr = str(b_cur).zfill(3)
                # print("\n%s) Counts: %s" % (posstr, " ".join(context)))
                # print(  "%s) %s" % (posstr, out))        
                # print(  "%s) W1: %s; W2: %s; W3: %s" % (posstr,w1, w2, w3))
                # print(num_words, sum(wordcounts.values()))

                # Always insert boundaries at utterance boundaries
                if b_cur in U:
                    insert_boundary = True
                else:
                    # Counts of words in the focus
                    num_w1 = wordcounts[w1]
                    num_w2 = wordcounts[w2]
                    num_w3 = wordcounts[w3]
                    # Is w_1 utterance final?
                    w1_is_final = (b_next in U)
                    # Count the number of utterences in the focus area
                    total_num_u = len(U) - 1

                    num_u_in_focus = (b_prev in U and b_prev != 0) + (w1_is_final and b_next != last_U)
                    num_u_context = total_num_u - num_u_in_focus
                    num_u = num_u_context if w1_is_final else num_words - num_u_context

                    # if the probability for this sequence has already
                    # been computed - retrieve it from the dictionary
                    if w1 in prob_dict:
                        p0_w1 = prob_dict[w1]
                    else:
                        # otherwise memoise it for later use
                        p0_w1 = P0(w1)
                        prob_dict[w1] = p0_w1

                    # Probability of not inserting a boundary
                    prob_h1  = (num_w1 + alpha * p0_w1) / (num_words + alpha)
                    prob_h1 *= (num_u + rho/2) / (num_words + rho)

                    # if the probability for this sequence has already
                    # been computed - retrieve it from the dictionary
                    if w2 in prob_dict:
                        p0_w2 = prob_dict[w2]
                    else:
                        # otherwise memoise it for later use
                        p0_w2 = P0(w2)
                        prob_dict[w2] = p0_w2

                    # if the probability for this sequence has already
                    # been computed - retrieve it from the dictionary
                    if w3 in prob_dict:
                        p0_w3 = prob_dict[w3]
                    else:
                        # otherwise memoise it for later use
                        p0_w3 = P0(w3)
                        prob_dict[w3] = p0_w3

                    # Prob of inserting a boundary
                    prob_h2  = ((num_w2 + alpha * p0_w2) / (num_words + alpha)
                                * (num_words - total_num_u + rho/2) / (num_words + rho))
                    prob_h2 *= ((num_w3 + int(w2 == w3) + alpha * p0_w3) / (num_words + 1 + alpha)
                                * (num_u + (1 - w1_is_final) + rho/2) / (num_words + 1 + rho))
                                # using (1-w1_is_final) = int(w2_is_final == w1_is_final)

                    insert_boundary = prob_h2 > prob_h1

                # Update wordcounts
                if insert_boundary:
                    wordcounts[w2] += 1
                    num_words += 1
                    B[b_cur] = 1

                    # (*) Save previous boundary position and whether it is in U
                    b_prev = b_cur
                else:
                    B[b_cur] = 0

        self.wordcounts = wordcounts + Counter()          
        end_time = time.time() - start_time
        print('     End sampling')
        print('TIME ELAPSED:', end_time)

        file_name = 'final_results_training_'+str(self.sample_call_id)+'.txt'
        with open(file_name, 'a+') as h:
            h.write('<Final boundaries:>')
            h.write(str(B))
            h.write('\n\n')

        return B



if __name__ == '__main__':
    file_name = "data" + os.path.sep + "br-phono-train.txt"

    training_no = 2
    avg_word_len, bound_prob, phon_prob = 3, 0.5, 'uniform'
    
    # should amount to ~2.5h time (each iteration takes roughly 0.86 secs on Valentin's machine)
    num_iter = 5000

    
    # CHANGE THIS TO -1 FOR ALL UTTERANCES
    num_utterances = 10
    W = WordSegmenter(file_name, avg_word_len, bound_prob, phon_prob, N=num_utterances)
    W.sample_call_id = training_no
    
    # fixed - paper says they're the best parameters
    alpha, rho = 50, 2    
    B = W.sample(num_iter, alpha, rho)
    # B_new = [i for i, b in enumerate(B) if b == 1]
    