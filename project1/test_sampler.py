from helpers import *
from sampler import *
from FileUtils import read_data
from Initialisation import gather_uniform_phon_probs, initialise_poisson, initialise_random


if __name__ == '__main__':
    
    #### 
    ## A silly demo
    # Get corpus and utterance boundaries
    orig_corpus = "helloworld$hereisanicestory$helloworldnostorypleaseworld"
    corpus, U = clean_corpus(orig_corpus)

    # Our 'random' initialization of the boundaries with
    # utterance boundaries, no duplicates and sorted
    B = [5, 10, 12, 17, 25, 31, 36, 49]
    B = sorted(set(B + U))

    P0 = lambda w: 1
    alpha, rho = 1, 2
    print(Sampler(corpus, B, U, 4, P0, alpha, rho))

 
    ###
    # Some more involved stuff that doesn't run at Bas's computer

    # data is a list of strings
    data = read_data('data\\br-phono-test.txt')
    data = ['helloworld', 'helloplanet', 'byeworld', 'byeplanet']

    # computes the probabilities of all phonemes and returns a function
    # which computes the probability of a sequence based on these probabilities
    uni_prob = gather_uniform_phon_probs(data, 0.5)

    # randomly generates word boundaries
    B = list(initialise_poisson(data, 4))

    # prepare data for function 'clean_corpus'
    data = '$'.join((line for line in data))

    corpus, U = clean_corpus(data)

    B = sorted(set(B + U))

    # get a shallow copy of B - just to be sure that it is not canged by the sampler
    B_copy = B[:]

    result = Sampler(corpus, B, U, 10000, uni_prob, alpha, rho)

    # print the data with the initial word boundaries
    print(''.join(['_'+corpus[i] if i in B_copy else corpus[i] for i in range(len(corpus))]))

    # print the data with the inferred word boundaries
    print(''.join(['_'+corpus[i] if i in result else corpus[i] for i in range(len(corpus))]))