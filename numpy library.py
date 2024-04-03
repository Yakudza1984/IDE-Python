import numpy as np

a = np.array([23,34,27])
b = np.array([-54,1,46])
c = np.array([46,68,54])

def isCorrect(v1, v2):
    return np.linalg.norm(v1) + np.linalg.norm(v2) == np.linalg.norm(v1 + v2)

def moreThan100(v1, v2):
    return np.linalg.norm(v1 - v2) > 100

def isDot(v1, v2):
    return np.dot(v1,v2) == 0

np.random.seed(2021)
simple = np.random.uniform()
randoms = np.random.randint(-150,2021, size=120)
table = np.random.randint(1,101, size=(3,2))
even = np.arange(2,17, step=2)
mix = np.random.permutation(even)
select = np.random.choice(even, size=3, replace=False)
triplet = np.random.permutation(select)
print(mix)