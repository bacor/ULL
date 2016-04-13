from helpers import *
from collections import Counter

def Gibbygibbs(corpus, B, num_iter, P0, alpha, rho):
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

    for t in range(num_iter):
        print("Starting iteration %s" % t)

        # Remove first word from focus
        W_after[corpus[:B[1]]] -= 1 

        for b_cur in range(1,len(corpus)+1):

            # Is b_cur on the boundary?
            cur_is_on_boundary = (b_cur in B)

            # To do: make more efficient?
            b_prev = max([b for b in B if b < b_cur])

            if b_cur == len(corpus):
                b_next = len(corpus)
            else:
                b_next = min([b for b in B if b > b_cur])

            # Words/fragments in the focus
            w1 = corpus[b_prev:b_next]
            w2 = corpus[b_prev:b_cur]
            w3 = corpus[b_cur:b_next]

            # We moved to a boundary, remove w3 from W_after
            if cur_is_on_boundary:
                W_after[w3] -= 1
                num_words = len(B) - 3
            else:
                num_words = len(B) - 2

            # Counts of words in the focus
            num_w1 = W_before[w1] + W_after[w1]
            num_w2 = W_before[w2] + W_after[w2]
            num_w3 = W_before[w3] + W_after[w3]    

            # For debugging (ONLY ON SMALL CORPORA!)
#             corpus2 = add_word_boundaries(corpus, sorted(B))
#             new_B = [b+i for i,b in enumerate(B)]
#             new_b_cur = b_cur + len([b for b in B if b < b_cur])
#             # This prints the corpus with word boundaries,
#             print(("%s) "%b_cur)+corpus2[:new_b_cur] + '|'+corpus2[new_b_cur:])
#             print("\tBefore: " + " ".join(["%s(%s)" %(w,i) for w, i in W_before.items() if i>0]))    
#             print("\tAfter: " + " ".join(["%s(%s)" %(w,i) for w, i in W_after.items() if i>0]))

            # Is w_1 utterance final?
            w1_is_final = (b_next in U)
            w2_is_final = (b_cur in U)
            w3_is_final = (b_next in U) # Weird: this is just w1_is_final

            # num(utterance boundaries in the context)
            num_utterances = len([u for u in U if (u <= b_prev or u > b_next) and u != 0])
            num_u = num_utterances if w1_is_final else num_words - num_utterances

            # Question: Should we use log probs for overflow ?!
            # Probability of not inserting a boundary
            prob_h1  = (num_w1 + alpha * P0(w1)) / (num_words + alpha)
            prob_h1 *= (num_u + rho/2) / (num_words + rho)

            # Prob of inserting a boundary
            prob_h2  = ((num_w2 + alpha * P0(w2)) / (num_words + alpha)
                         * (num_words - num_utterances + rho/2) / (num_words + rho))
            prob_h2 *= ((num_w3 + int(w2 == w3) + alpha * P0(w3)) / (num_words + 1 + alpha)
                         * (num_u + int(w2_is_final == w3_is_final) + rho/2) / (num_words + 1 + rho))

            insert_boundary = (prob_h2 > prob_h1)

            # Always insert boundaries at utterance boundaries ?!?!
            if b_cur in U:
                insert_boundary = True

            # Update the contexts
            if not cur_is_on_boundary:
                if insert_boundary:
                    B += [b_cur]
                    W_after[w3] -= 1
                    W_before[w2] += 1
                # Else: don't do anything

            else: 
                if not insert_boundary:
                    index = B.index(b_cur)
                    del B[index]
                else:
                    W_before[w2] += 1

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
    print(Gibbygibbs(corpus, B, 4, P0, alpha, rho))
