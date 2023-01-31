# from graph import Graph

# # filename = "5eil51"
# # # g = Graph(f"Large Instances\\Type_1_Large\\{filename}.txt")
# # g = Graph(f"Small Instances\\Type_1_Small\\{filename}.txt")

# from individual import Individual
# from random import Random

# from utils.crossover import crossover_ox
# from utils.mutation import mutate

# g = Graph("test3.txt")
# # g = Graph(f"Small Instances\\Type_1_Small\\5eil51.txt")

# leng = len(g.steiner_vertexes)
# indi1 = Individual(leng)
# indi1.from_list([i for i in range(leng)])

# from utils.decoder import decode
# a = decode(indi1, g)

# for k in range(len(a)):
#     print("%2d" %(k),end="   ")
#     row = a[k]
#     for i in range(len(row)):
#         if row[i]:
#             print("%2d" %(i),end="   ")
#         else:
#             print(".",end="   ")
#     print()
        

# X = [234,346,74,435]
# Y = [1,4,3,2]
# a = [x for _, x in sorted(zip(Y, X), key=lambda pair: pair[0])]
# print(a)

print(3**0.5)