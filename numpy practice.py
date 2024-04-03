import numpy as np

def get_unique_loto(num):
    lst = []
    for i in range(num):
        lst.append(np.random.choice(101, (5, 5),replace=False))    
    return np.array(lst)

a = get_unique_loto(10)

check = []
for i in a:
  check.append(len(set(i.flatten())))




print(check)