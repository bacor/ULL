

import numpy as np


# data is a list of strings - each string is one line in the data
def initialise_random(data, boundary_param):

    for line in data:
        num_boundaries = np.random.poisson(len(line)/2)
        boundary_indices = np.random.choice(len(line), num_boundaries)
        print(line)
        print(boundary_indices)


if __name__ == '__main__':
    d = ['abcdefgh', 'valentin', 'amsterdam']

    initialise_random(d, 4)