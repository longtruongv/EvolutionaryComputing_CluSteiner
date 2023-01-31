import random
from itertools import islice


n = 5
# n_cluster = random.randint(3, 7)
n_cluster = 1

graph = [[0] * n for _ in range(n)]

for i in range(n):
    for j in range(i):
        a = random.randint(5, 1000)
        graph[i][j] = a
        graph[j][i] = a

for i in range(n):
    for j in range (n):
        print("{:10}".format(graph[i][j]), end = " ")
    print()

vertexes = [i+1 for i in range(n)]

def divide(lst, min_size, split_size):
    random.shuffle(lst)
    it = iter(lst)
    size = len(lst)
    for i in range(split_size - 1, 0, -1):
        s = random.randint(min_size, size -  min_size * i)
        yield list(islice(it,0,s))
        size -= s
    yield list(it)

clusters = list(divide(vertexes, 2, n_cluster+1))
for i in range(len(clusters) - 1): 
    print(i+1, end = " ")
    for v in clusters[i]:
        print(v, end = " ")

    print("-1")


