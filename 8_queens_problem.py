import random
import numpy as np
import math

from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from bitstring import BitArray



creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)





toolbox = base.Toolbox()
# Attribute generator 
toolbox.register("attr_bool", random.randint, 0, 1)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 64)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)




def check_queen_colision(x, y, m):
    """checa se há colisoes de rainhas numa dada coordenada a matriz

    Args:
        x (int): coordenada x
        y (int): coordenada y
        m (np.array(2x2)): matriz

    Returns:
        bool: True se há colisões, False se não
    """
    row = np.array(m[x,:])
    column = np.array(m[:,y])
    diag_1 = np.array(m).diagonal(y - x)
    dim = (len(m)-1)
    diag_2 = np.fliplr(m).diagonal( (dim - y) - x)
    
    array = np.concatenate((row, column, diag_1, diag_2))
    count = len([i for i in array if i > 0])
    if count > 4:
        return True
    return False
    

def funcao_objetivo(individual):
    """retorna o score de um individuo, baseado no número
    de rainhas que não apresentam

    Args:
        individual (tuple(n^2)): tupla com 1s e 0s, 1 = com rainha, 0 = sem rainha
    
    Returns:
        [int]: lista no shape (1,), com o score do individuo
    """
    dim = int(math.sqrt(len(individual)))
    matrix = np.array(individual).reshape(dim,dim)
    score = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i,j] == 1:
                colision = check_queen_colision(0,1,matrix)
                if not colision:
                    score += 1
    return [score]





toolbox.register("evaluate", funcao_objetivo)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)






def main():
    random.seed(64)
    
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, stats=stats, halloffame=hof, verbose=True)
    
    return pop, log, hof




if __name__ == "__main__":
    results = main()
    
    print(results[0])