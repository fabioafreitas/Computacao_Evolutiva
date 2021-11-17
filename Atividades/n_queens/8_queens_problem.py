import random
import numpy as np
import math

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

from bitstring import BitArray
import matplotlib.pyplot as plt
from numpy.core.numeric import count_nonzero


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
    

def count_queens_colisions(individual):
    """retorna o score de um individuo, baseado no número
    de rainhas que não apresentam

    Args:
        individual (tuple(n^2)): tupla com 1s e 0s, 1 = com rainha, 0 = sem rainha
    
    Returns:
        [int]: lista no shape (1,), com o score do individuo
    """
    n_queens = int(math.sqrt(len(individual)))
    count_queens = len([i for i in individual if i == 1])
    if count_queens != n_queens:
        return count_queens**count_queens,
    
    matrix = np.array(individual).reshape(n_queens,n_queens)
    score = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i,j] == 1:
                colision = check_queen_colision(i,j,matrix)
                if colision:
                    score += 1
    return score,

def generate_binary_n_queens_board(num_queens):
    """Generates a chess board with N queens plached whithin it
    will be place only queen per row and column

    Args:
        num_queens (int): number of queens

    Returns:
        tuple: (num_queens^2)
    """
    list_queen_position = random.sample(range(num_queens),num_queens)
    individual = []
    for index in range(num_queens):
        board_row = [0] * num_queens
        board_row[list_queen_position[index]] = 1
        individual += board_row
    return tuple(individual)



if __name__ == "__main__":
    NB_QUEENS = 8
    
    # run EA
    pop, log, _ = main(NB_QUEENS)
    print(pop)
    
    # plot
    gen = log.select('gen')
    best_per_gen = log.select('min')
    
    fig, ax = plt.subplots()
    ax.plot(gen, best_per_gen)
    ax.grid()
    ax.set(xlabel="Gerações", ylabel="Melhor Fitness")
    plt.show()