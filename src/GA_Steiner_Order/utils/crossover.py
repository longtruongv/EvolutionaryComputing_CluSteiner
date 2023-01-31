from random import Random

from individual import Individual

def crossover_ox(indi1: Individual, indi2: Individual, rand: Random):
    chromosome_len = indi1.length

    child1 = Individual(chromosome_len)
    child2 = Individual(chromosome_len)
    
    # print(chromosome_len)
    a = chromosome_len-1
    end = rand.randrange(2, a)
    start = rand.randrange(1, end)
    
    # print(start, end)

    for i in range(start, end+1):
        child1.set(i, indi1.get(i))
        child2.set(i, indi2.get(i))

    curr_idx_child1 = 0
    curr_idx_child2 = 0
    
    for i in range(chromosome_len):
        curr_idx = (end + i) % chromosome_len
        
        curr_gene_indi2 = indi2.get(curr_idx)
        if curr_gene_indi2 not in child1.chromosome:
            child1.set(curr_idx_child1, curr_gene_indi2)
            while True:
                curr_idx_child1 = (curr_idx_child1 + 1) % chromosome_len
                if (curr_idx_child1 < start or curr_idx_child1 > end):
                    break
        
        curr_gene_indi1 = indi1.get(curr_idx)
        if curr_gene_indi1 not in child2.chromosome:
            child2.set(curr_idx_child2, curr_gene_indi1)
            while True:
                curr_idx_child2 = (curr_idx_child2 + 1) % chromosome_len
                if (curr_idx_child2 < start or curr_idx_child2 > end):
                    break
    
    return child1, child2