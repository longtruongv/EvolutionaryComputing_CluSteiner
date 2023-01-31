from random import Random
from tqdm import tqdm

from graph import Graph
from individual import Individual
from population import Population

from utils.crossover import crossover_ox
from utils.mutation import mutate
from utils.logger import Logger

class GeneticAlgorithm:
    def __init__(self, 
        filename,
        seed,
        logger: Logger,
        generation, 
        population_size,
        crossover_rate,
        mutation_rate,
    ):
        self.seed = seed
        self.random = Random(seed)

        self.logger = logger

        self.graph = Graph(filename)
        self.population = Population(population_size)
        self.init_population()

        self.generation = generation
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

        self.stop = False

    def init_population(self, ):
        chromosome_len = len(self.graph.steiner_vertexes)
        chromosome = [i for i in range(chromosome_len)]

        for i in range(self.population.size):
            self.random.shuffle(chromosome)
            indi = Individual()
            indi.from_list(chromosome)
            indi.calcu_fitness(self.graph)

            self.population.set(i, indi)

        self.bestfit_indi = self.population.get(0)

    def run_algorithm(self):
        pbar = tqdm(range(self.generation), desc=f'Seed: {self.seed}')
        for i in pbar:
            if (self.stop):
                break

            crossover_children = self.make_crossover()
            mutation_children = self.make_mutation()
            
            self.calcu_new_population(crossover_children, mutation_children)
            self.eval_population()

            bestfound = 1 - self.bestfit_indi.fitness
            average = 1 - self.population.fitness

            self.logger.apend_log(self.seed, i, bestfound, average)
            pbar.set_postfix(bestfound=bestfound, average=average)


    def eval_population(self):
        popu_fitness = 0
        for indi in self.population.individuals:
            popu_fitness += indi.fitness
            if (indi.fitness > self.bestfit_indi.fitness):
                self.bestfit_indi = indi

            avg_fitness = popu_fitness / self.population.size
            self.population.fitness = avg_fitness

    def calcu_new_population(self, crossover_children, mutation_children):
        new_generation = self.population.individuals
        new_generation.extend(crossover_children)
        new_generation.extend(mutation_children)

        new_generation = sorted(new_generation, key=lambda x: x.fitness, reverse=True)

        bestfit_count = int(self.population.size * 0.8)
        bestfit = new_generation[:bestfit_count]

        remain_count = self.population.size - bestfit_count
        remain = new_generation[bestfit_count:]
        remain = self.random.sample(remain, remain_count)

        bestfit.extend(remain)
        self.population.individuals = bestfit


    def make_crossover(self):
        num_parent = int(self.population.size * self.crossover_rate)
        if num_parent % 2 == 1:
            num_parent -= 1

        parent = self.random.sample(self.population.individuals, num_parent)
        children = []

        for i in range(1, num_parent, 2):
            child1, child2 = crossover_ox(parent[i-1], parent[i], self.random)
            child1.calcu_fitness(self.graph)
            child2.calcu_fitness(self.graph)

            children.append(child1)
            children.append(child2)

        return children

    def make_mutation(self):
        num_parent = int(self.population.size * self.mutation_rate)
        parent = self.random.sample(self.population.individuals, num_parent)
        children = []

        for i in range(num_parent):
            child = mutate(parent[i], self.random)
            child.calcu_fitness(self.graph)

            children.append(child)

        return children



    
    
