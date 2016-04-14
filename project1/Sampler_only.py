from helpers import *
from collections import Counter

def Sampler(corpus, B, U, num_iter, P0, alpha, rho):
    """Gibbs sampler

    Args:
        corpus: a very long string without utterance boundaries
        B: list of boundary positions
        num_iter: number of iterations
        P0: a function that takes a word and returns a probability
        alpha: the alpha hyperparam
        rho: the rho param

    Returns:
        Returns the boundary positions
    """

    # Initialize words
    W_before = Counter()
    W_after = get_words_counts(corpus, B)
    total_utterances = len(U)

    for t in range(num_iter):
        #         print("Starting iteration %s" % t)

        # Remove first word from focus
        W_after[corpus[:B[1]]] -= 1 
        b_prev_index = 0

        for b_cur in range(1,len(corpus)+1):
            b_prev = B[b_prev_index]
            b_next = B[b_prev_index + 1]

            # Words/fragments in the focus
            w1 = corpus[b_prev:b_next]
            w2 = corpus[b_prev:b_cur]
            w3 = corpus[b_cur:b_next]

            # Is b_cur on the boundary?
            cur_is_on_boundary = (b_cur in B)

            # We moved to a boundary, remove w3 from W_after
            if cur_is_on_boundary:
                W_after[w3] -= 1
                num_words = len(B) - 3
            else:
                num_words = len(B) - 2

            # Always insert boundaries at utterance boundaries ?!?!
            if b_cur in U:
                insert_boundary = True

            else:
                # Counts of words in the focus
                num_w1 = W_before[w1] + W_after[w1]
                num_w2 = W_before[w2] + W_after[w2]
                num_w3 = W_before[w3] + W_after[w3]    

                # Is w_1 utterance final?
                w1_is_final = (b_next in U)

                # Count the number of utterences in the focus area
                total_num_u = len(U) - 1
                num_u_in_focus = (b_prev in U and b_prev != 0) + (w1_is_final and b_next != U[-1])
                num_u_context = total_num_u - num_u_in_focus
                num_u = num_u_context if w1_is_final else num_words - num_u_context

                # Probability of not inserting a boundary
                prob_h1  = (num_w1 + alpha * P0(w1)) / (num_words + alpha)
                prob_h1 *= (num_u + rho/2) / (num_words + rho)

                # Prob of inserting a boundary
                prob_h2  = ((num_w2 + alpha * P0(w2)) / (num_words + alpha)
                             * (num_words - total_num_u + rho/2) / (num_words + rho))
                prob_h2 *= ((num_w3 + int(w2 == w3) + alpha * P0(w3)) / (num_words + 1 + alpha)
                             * (num_u + (1 - w1_is_final) + rho/2) / (num_words + 1 + rho))
                # We used int(w2_is_final == w1_is_final) = 1- w1_is_final

                insert_boundary = prob_h2 > prob_h1


            # Update the contexts
            if not cur_is_on_boundary:
                if insert_boundary:
                    # Insert boundary at right position (keep B ordered)
                    B.insert(b_prev_index + 1, b_cur)
                    b_prev_index += 1
                    W_after[w3] -= 1
                    W_before[w2] += 1
                # Else: don't do anything

            else: 
                if not insert_boundary:
                    index = B.index(b_cur)
                    del B[index]
                else:
                    W_before[w2] += 1
                    b_prev_index += 1            

        # Wrap up this iteration
        W_after = W_before
        W_before = Counter()

    return B



    

if __name__ == '__main__':
    
    orig_corpus = "helloworld$hereisanicestory$helloworldnostorypleaseworld"

    # Get corpus and utterance boundaries
    corpus, U = clean_corpus(orig_corpus)

    # Our 'random' initialization of the boundaries with
    # utterance boundaries, no duplicates and sorted
    B = [5, 10, 12, 17, 25, 31, 36, 49]
    B = sorted(set(B + U))

    P0 = lambda w: 1
    alpha = 1
    rho = 2
    print(Sampler(corpus, B, U, 4, P0, alpha, rho))
