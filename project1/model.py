from helpers import *
from collections import Counter

import cProfile, pstats, io

class WordSegmenter:
    """WordSegmenter class implements the model"""

    def __init__(self, corpus):
        """Initialize the class

        Args:
            corpus: an uncleaned corpus (raw text with utterance boundaries etc)
        """
        self.corpus, self.U = clean_corpus(corpus)

    def initialize(self, B):
        """Initialize the model"""

        ## Put initialization here at some point
        B = sorted(set(B + self.U))
        return B

    def sample(self, B, num_iter, P0, alpha, rho):
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

        prob_dict = {}


        pr = cProfile.Profile()

        pr.enable()

        import time

        start_time = time.time()

        last_index = 0

        U = self.U
        corpus = self.corpus

        # Initialize wordcounts
        wordcounts = get_words_counts(corpus, B)



        for t in range(num_iter):
            # Remove first word and (occasionally) all nonpositive ones
            wordcounts[corpus[:B[1]]] -= 1 
            if (t % 20) == 0: 
                wordcounts += Counter()
            b_prev_index = 0
            
            for b_cur in range(1,len(corpus)+1):
                # Is b_cur on the boundary?
                cur_is_on_boundary = (b_cur in B)

                # Previous and next boundaries
                b_prev = B[b_prev_index]
                next_index = min(b_prev_index + 1 + int(cur_is_on_boundary), len(B)-1)
                b_next = B[next_index]

                # Words/fragments in the focus area
                w1 = corpus[b_prev:b_next]
                w2 = corpus[b_prev:b_cur]
                w3 = corpus[b_cur:b_next]

                # Update wordcounts and #words in context
                wordcounts[w3] -= int(cur_is_on_boundary)
                num_words = len(B) - 2 - int(cur_is_on_boundary)
                            
                # Always insert boundaries at utterance boundaries ?!?!
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
                    num_u_in_focus = (b_prev in U and b_prev != 0) + (w1_is_final and b_next != U[-1])
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

# < <<<<<< Updated upstream
                    # Update the contexts
                    if cur_is_on_boundary: 
                        if insert_boundary:
                            wordcounts[w2] += 1
                            b_prev_index += 1
                        else:
                            # index = B.index(b_cur)



                            index = [i for i in range(last_index, min(last_index+1000, len(B))) if B[i] == b_cur]

                            if len(index) != 1:
                                print('WHAT THE FUCK: ', index)

                            # print('b_cur', b_cur, "   b_cur's index", index)
                            del B[index[0]]

                            last_index = index[0]
                    elif insert_boundary:
                        # Insert boundary at the right position to keep B ordered
                        B.insert(b_prev_index + 1, b_cur)
                        b_prev_index += 1
# # = ======
#                 # Update the contexts
#                 if cur_is_on_boundary: 
#                     if insert_boundary:
# > >>>>>> Stashed changes
                        wordcounts[w2] += 1
                        b_prev_index += 1
                    else:
                        index = B.index(b_cur)
                        del B[index]

                elif insert_boundary:
                    # Insert boundary at the right position to keep B ordered
                    B.insert(b_prev_index + 1, b_cur)
                    b_prev_index += 1
                    wordcounts[w2] += 1

                # DEBUGGIN of a SMALL corpus!
                # This prints the corpus with word boundaries,
                # corpus2 = add_word_boundaries(corpus, sorted(B))
                # new_B = [b+i for i,b in enumerate(B)]
                # new_b_cur = b_cur + len([b for b in B if b < b_cur])
                # next_context = ["%s(%s)" % (w,i) for w, i in wordcounts.items() if i>0]
                # print(("\n%s) " % b_cur) + corpus2[:new_b_cur] + ' | ' + corpus2[new_b_cur:])
                # print("Next context: " + " ".join(next_context))

        pr.disable()

        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

        end_time = time.time() - start_time

        print('TIME ELAPSED:', end_time)

        return B


def Sampler(corpus, B, U, num_iter, P0, alpha, rho):
    """DEPRECATED Function to sample from model. Use model class instead."""
    raw_corpus = ""
    prev_u = 0
    for u in U:
        raw_corpus += corpus[prev_u:u] + "$"
        prev_u = u    
    W = WordSegmenter(raw_corpus)
    B = W.initialize(B)
    return W.sample(B, num_iter, P0, alpha, rho)
    

if __name__ == '__main__':
    
    orig_corpus = "helloworld$hereisanicestory$helloworldnostorypleaseworld"

    W = WordSegmenter(orig_corpus)
    B = W.initialize([5, 10, 12, 17, 25, 31, 36, 49])

    P0 = lambda w: 1
    alpha = 1
    rho = 2
    print(W.sample(B, 4, P0, alpha, rho))
