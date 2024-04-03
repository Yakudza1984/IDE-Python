from collections import defaultdict, deque

tasks = [(36871, 'office', False),
(40690, 'office', False),
(35364, 'voltage', False),
(41667, 'voltage', True),
(33850, 'office', False)]

def task_manager(tasks):
    dc = defaultdict(deque)
    for x,y,z in tasks:
        if z == True:
            dc[y].appendleft(x)
        else:
            dc[y].append(x)    
        
    return dc
print(task_manager(tasks))