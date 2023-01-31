from random import Random

from individual import Individual

MUTATION_COEF = 10

def mutate(indi: Individual, rand: Random):
    chromosome_len = indi.length

    child = Individual(chromosome_len)
    child.from_list(indi.chromosome)

    count = rand.randrange(1, MUTATION_COEF)

    while count > 0:
        p1 = rand.randrange(1, chromosome_len);
        p2 = rand.randrange(0, p1)

        temp = child.get(p1)
        child.set(p1, child.get(p2))
        child.set(p2, temp)

        count -= 1

    return child

