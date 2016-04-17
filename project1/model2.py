from helpers import *
from Initialisation import *

class WordSegmenter:
    """WordSegmenter class implements the model"""

    def __init__(self, corpus_file, avg_word_length, boundary_prob, phon_prob='uniform'):
        """Initialize the class

        Args:
            corpus: an uncleaned corpus (raw text with utterance boundaries etc)
        """

        self.corpus = read_data(corpus_file)

        if phon_prob == 'uniform':
            P0 = gather_uniform_phon_probs(self.corpus, boundary_prob)
        elif phon_prob == 'unigram':
            P0 = gather_unigram_phon_probs(self.corpus, boundary_prob)
        elif phon_prob == 'bigram':
            P0 = gather_bigram_phon_probs(self.corpus, boundary_prob)
        else:
            raise ValueError('Phoneme probability measure must be one of: uniform, unigram, bigram.')

        self.P0 = P0

        B = set(initialise_poisson(self.corpus, avg_word_length))

        self.corpus = '$'.join((line for line in self.corpus))

        self.corpus, self.U = clean_corpus(self.corpus)

        B |= set(self.U)

        B = [1 if i in B else 0 for i in range(len(self.corpus)+1)]

        self.B = B

    def get_next_bound(self, pos):
            return next(i for i in range(pos, len(self.B)) if self.B[i] == 1)

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

        prob_dict = {}

        B = self.B

        num_boundaries = sum(B) - 2

        P0 = self.P0

        start_time = time.time()

        U = self.U
        last_U = U[-1]
        U = set(U)

        corpus = self.corpus

        # Initialize wordcounts
        wordcounts = get_words_counts(corpus, B)

        print('Start sampling')

        for t in range(num_iter):

            if (t % 100) == 0:
                print('<Boundaries at iteration: ', t, '>: ', B)

            # Remove first word and (occasionally) all nonpositive ones
            wordcounts[corpus[:self.get_next_bound(0)]] -= 1
            if (t % 20) == 0:
                wordcounts += Counter()
            b_prev_index = 0


            for b_cur in range(1,len(corpus)+1):

                # Is b_cur on the boundary?
                cur_is_on_boundary = (B[b_cur] == 1)

                # Previous and next boundaries
                b_prev = self.get_prev_bound(b_cur)
                b_next = self.get_next_bound(b_cur)

                t2 = time.time()
                # Words/fragments in the focus area
                w1 = corpus[b_prev:b_next]
                w2 = corpus[b_prev:b_cur]
                w3 = corpus[b_cur:b_next]

                # Update wordcounts and #words in context
                wordcounts[w3] -= int(cur_is_on_boundary)
                num_words = num_boundaries - 2 - int(cur_is_on_boundary)


                # Always insert boundaries at utterance boundaries
                if not b_cur in U:
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

                    # Update the contexts
                    if cur_is_on_boundary: 
                        if insert_boundary:
                            wordcounts[w2] += 1
                            b_prev_index += 1
                        else:
                            B[b_cur] = 0
                            num_boundaries -= 1
                    elif insert_boundary:
                        # Insert boundary at the right position to keep B ordered
                        B[b_cur] = 1
                        b_prev_index += 1
                        wordcounts[w2] += 1
                        num_boundaries += 1

                # DEBUGGING of a SMALL corpus!
                # This prints the corpus with word boundaries,
                # corpus2 = add_word_boundaries(corpus, sorted(B))
                # new_B = [b+i for i,b in enumerate(B)]
                # new_b_cur = b_cur + len([b for b in B if b < b_cur])
                # next_context = ["%s(%s)" % (w,i) for w, i in wordcounts.items() if i>0]
                # print(("\n%s) " % b_cur) + corpus2[:new_b_cur] + ' | ' + corpus2[new_b_cur:])
                # print("Next context: " + " ".join(next_context))


        end_time = time.time() - start_time
        print('TIME ELAPSED:', end_time)

        return B