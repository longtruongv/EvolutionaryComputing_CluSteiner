from random import Random
from tqdm import tqdm

from graph import Graph
from individual import Individual
from population import Population

from utils.crossover import crossover_sbx
from utils.mutation import mutate
from utils.logger import Logger

RMP = 0.3

class MFEA:
    def __init__(self, 
        filenames: list[str],
        seed: int,
        logger: Logger,
        generation: int, 
        population_size: int,
    ):
        self.seed = seed
        self.random = Random(seed)

        self.logger = logger

        self.graphs = [Graph(filename) for filename in filenames]
        self.num_problem = len(filenames)

        self.population = Population(population_size, self.num_problem)
        self.init_population()

        self.generation = generation

        self.stop = False

    def init_population(self, ):
        chromosome_len = max([g.num_steiner_vertexes for g in self.graphs])

        for i in range(self.population.size):
            chromosome = [self.random.random() for _ in range(chromosome_len)]
            indi = Individual()
            indi.from_list(chromosome)

            indi.calcu_factorial_cost(self.graphs)

            self.population.set(i, indi)

        self.bestfit_indi: list[Individual] = []
        for i in range(self.num_problem):
            self.bestfit_indi.append(self.population.sort_by_factorial_cost(i)[0])

    def run_algorithm(self):
        pbar = tqdm(range(self.generation), desc=f'Seed: {self.seed}')
        for i in pbar:
            if (self.stop):
                break

            children = self.make_new_generation()
            
            self.calcu_new_population(children)
            self.eval_population()

            bestfounds = [bf.factorial_cost[i] for i, bf in enumerate(self.bestfit_indi)]
            averages = self.population.averages

            self.logger.apend_log(self.seed, i, bestfounds, averages)

            pbar.set_postfix(bestfound=bestfounds, average=averages)


    def eval_population(self):
        popu_total = [0] * self.num_problem
        counting = [0] * self.num_problem
        for indi in self.population.individuals:         
            for i in range(self.num_problem):
                if indi.get_skill_factor() == i:
                    popu_total[i] += indi.factorial_cost[i]
                    counting[i] += 1

                    if indi.factorial_cost[i] < self.bestfit_indi[i].factorial_cost[i]:
                        self.bestfit_indi[i] = indi

        popu_averages = [-1] * self.num_problem
        for i in range(self.num_problem):
            if counting[i] > 0:
                popu_averages[i] = popu_total[i] / counting[i]

        self.population.averages = popu_averages

    def calcu_new_population(self, children:list[Individual]):
        for i in range(self.num_problem):
            self.population.sort_by_factorial_cost(i, children)

        new_generation = self.population.sort_by_scalar_fitness(children)

        # bestfit_count = int(self.population.size * 0.8)
        # bestfit = new_generation[:bestfit_count]

        # remain_count = self.population.size - bestfit_count
        # remain = new_generation[bestfit_count:]
        # remain = self.random.sample(remain, remain_count)

        # bestfit.extend(remain)
        self.population.individuals = new_generation[:self.population.size] # bestfit
        

    def make_new_generation(self):
        parent = self.population.individuals
        self.random.shuffle(parent)

        children = []

        for i in range(1, self.population.size, 2):
            p1 = parent[i-1]
            p2 = parent[i]

            r1 = self.random.random()
            if (p1.get_skill_factor() == p2.get_skill_factor()) or (r1 < RMP):
                child1, child2 = crossover_sbx(p1, p2, self.random)
                
                self.valuate_child(child1, p1, p2)
                self.valuate_child(child2, p1, p2)
            else:
                child1 = mutate(p1, self.random)
                self.valuate_child(child1, p1)

                child2 = mutate(p2, self.random)
                self.valuate_child(child2, p2)

            children.append(child1)
            children.append(child2)

        return children
            
                
    def valuate_child(self, c:Individual, p1:Individual, p2:Individual=None):
        if p2 is not None:
            r = self.random.random()
            if (r < 0.5):
                problem_id = p1.get_skill_factor()
            else:
                problem_id = p2.get_skill_factor()
                
            c.calcu_factorial_cost(self.graphs, problem_id)
        else:
            problem_id = p1.get_skill_factor()
            c.calcu_factorial_cost(self.graphs, problem_id)




