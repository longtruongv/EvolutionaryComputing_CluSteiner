from datetime import datetime
import csv
import os

class Logger:
    def __init__(self, names):
        try:
            folder_name = "-".join(names)
            self.path_name = f"res\\output\\MFEA_{folder_name}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
            self.path = os.path.relpath(self.path_name)
            os.mkdir(self.path)
        except:
            pass

        self.full_log = {}

    def apend_log(self, seed, generation, bestfounds, averages):
        if seed not in self.full_log:
            self.full_log[seed] = []

        self.full_log[seed].append((generation, bestfounds, averages))

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

    def save_best_found(self, bestfounds):
        with open(f'{self.path_name}\\bestfound.txt', 'w') as file:
            for i, bf in enumerate(bestfounds):
                file.write(f"PROBLEM {i}\n")
                file.write(f"\tSeed : {bf[2]}\n")
                file.write(f"\tBest found : {bf[1]}\n")
                file.write(f"\tChromosome: ")
                for gene in bf[0]:
                    file.write(f"{gene}\t")
                file.write("\n")