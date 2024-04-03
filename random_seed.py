import numpy as np

def shuffle_seed(array):
    seed = np.random.randint(0, 2**32, 1, np.int64)
    np.random.seed(seed)
    n_array = np.random.permutation(array)
    return n_array, seed[0]

array = [1, 2, 3, 4, 5]
print(shuffle_seed(array))