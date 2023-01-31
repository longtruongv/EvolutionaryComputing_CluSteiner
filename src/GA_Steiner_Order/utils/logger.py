from datetime import datetime
import csv
import os

class Logger:
    def __init__(self, folder_name):
        try:
            self.path_name = f"res\\output\\GA_{folder_name}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
            self.path = os.path.relpath(self.path_name)
            os.mkdir(self.path)
        except:
            pass

        self.full_log = {}

    def apend_log(self, seed, generation, bestfound, average):
        if seed not in self.full_log:
            self.full_log[seed] = []

        self.full_log[seed].append((generation, bestfound, average))

    def save_log(self, seed=None):
        if seed is None:
            for seed in self.full_log:
                with open(f'{self.path_name}\\seed{seed}.csv', 'wb') as file:
                    csv_out = csv.writer(file)
                    csv_out.writerows(self.full_log[seed])
        else:
            if seed in self.full_log:
                with open(f'{self.path_name}\\seed{seed}.csv', 'w') as file:
                    csv_out = csv.writer(file)
                    csv_out.writerows(self.full_log[seed])

    def save_best_found(self, chromosome:list, fitness, seed):
        with open(f'{self.path_name}\\bestfound.txt', 'w') as file:
            file.write(f"Seed: {seed}\n")
            file.write(f"Best found: {1 - fitness}\n")
            file.write(f"Chromosome: ")
            for gene in chromosome:
                file.write(f"{gene}\t")