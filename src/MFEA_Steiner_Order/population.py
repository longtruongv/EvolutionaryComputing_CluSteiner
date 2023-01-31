import utils.constants as constants
from individual import Individual

class Population:
    def __init__(self, size, num_problem):
        self.size = size
        self.individuals:list[Individual] = [None] * size
        self.averages = [constants.MAX_INT for _ in range(num_problem)]

    def get(self, idx):
        if idx >= self.size:
            return None
        return self.individuals[idx]
    
    def set(self, idx, individual: Individual):
        if idx >= self.size:
            print("Insert Individual to Population FAILED!")
            return

        self.individuals[idx] = individual

    def sort_by_factorial_cost(self, problem_id:int, new_generation:list[Individual]=None):
        temp_population = self.individuals.copy()
        if new_generation is not None:
            temp_population.extend(new_generation)

        temp_population.sort(key=lambda x: x.factorial_cost[problem_id])

        for i in range(len(temp_population)):
            temp_population[i].factorial_rank[problem_id] = i

        return temp_population

    def sort_by_scalar_fitness(self, new_generation:list[Individual]=None):
        temp_population = self.individuals.copy()
        if new_generation is not None:
            temp_population.extend(new_generation)

        temp_population.sort(key=lambda x: x.get_scalar_fitness(), reverse=True)

        return temp_population

        
