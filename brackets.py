from collections import deque
def brackets(line=''):
    dq = deque()
    for elem in line:
        if elem == '(':
            dq.append(elem)
        elif elem == ')' and dq:
            dq.pop()
        else:
            return False
    
    return not dq

print(brackets('(()()))'))