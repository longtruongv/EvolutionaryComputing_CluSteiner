import utils.constants as constants
from individual import Individual

class Population:
    def __init__(self, size):
        self.size = size
        self.individuals:list[Individual] = [None] * size
        self.fitness = constants.MIN_INT

    def get(self, idx):
        if idx >= self.size:
            return None
        return self.individuals[idx]
    
    def set(self, idx, individual: Individual):
        if idx >= self.size:
            print("Insert Individual to Population FAILED!")
            return

        self.individuals[idx] = individual
        
