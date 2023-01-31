from genetic_algorithm import GeneticAlgorithm
from utils.logger import Logger

if __name__ == "__main__":
    instance_name = '5eil51' # 5eil51, 5berlin52, 10gil262, 10a280, 5eil76

    # filename = f"Large Instances\\Type_1_Large\\{instance_name}.txt"
    filename = f"Small Instances\\Type_1_Small\\{instance_name}.txt"
    
    logger = Logger(instance_name)

    for seed in range(30):
        ga = GeneticAlgorithm(filename, seed, logger, 500, 100, 0.8, 0.2)
        ga.run_algorithm()

        if seed == 0:
            bf = ga.bestfit_indi
            bf_seed = seed
        else:
            if ga.bestfit_indi.fitness > bf.fitness:
                bf = ga.bestfit_indi
                bf_seed = seed

        logger.save_log(seed)

    logger.save_best_found(bf.chromosome, bf.fitness, bf_seed)
    print(bf.chromosome, bf.fitness)

    
    