from MFEA import MFEA
from utils.logger import Logger

if __name__ == "__main__":
    instance_name1 = '10eil76' # 5eil51, 5berlin52, 5eil76
    filename1 = f"Small Instances\\Type_1_Small\\{instance_name1}.txt"

    instance_name3 = '5berlin52' # 5eil51, 5berlin52, 5eil76
    filename3 = f"Small Instances\\Type_1_Small\\{instance_name1}.txt"

    instance_name2 = '25a280' # 10a280, 10gil262, 10lin318
    filename2 = f"Large Instances\\Type_1_Large\\{instance_name2}.txt"
    
    logger = Logger([instance_name1, instance_name2, instance_name3])

    for seed in range(30):
        filenames = [filename1, filename2, filename3]
        mfea = MFEA(filenames, seed, logger, 500, 100)
        mfea.run_algorithm()

        if seed == 0:
            bestfounds = []
            for i, bf in enumerate(mfea.bestfit_indi):
                bestfounds.append((bf.chromosome, bf.factorial_cost[i], seed))
        else:
            for i, bf in enumerate(mfea.bestfit_indi):
                if bf.factorial_cost[i] < bestfounds[i][1]:
                    bestfounds[i] = (bf.chromosome, bf.factorial_cost[i], seed)

        logger.save_log(seed)

    logger.save_best_found(bestfounds)
    print(bestfounds)

    
    