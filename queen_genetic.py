#!/usr/bin/env python3
import random
from functools import reduce
from itertools import groupby
import time
import json
def random_chromosome(size): #making random chromosomes
    return [ random.randint(1, size) for _ in range(size)]

def fitness(chromosome, maxFitness):
    horizontal_collisions = sum([chromosome.count(queen)-1 for queen in chromosome])/2
    left_diagonal_collisions_mat = sorted(reduce(lambda x,y: x + [y - len(x)], chromosome, []))
    left_diagonal_collisions = [len(list(group)) for key, group in groupby(left_diagonal_collisions_mat)]
    right_diagonal_collisions_mat = sorted(reduce(lambda x,y: x + [y + len(x)], chromosome, []))
    right_diagonal_collisions = [len(list(group)) for key, group in groupby(right_diagonal_collisions_mat)]
    diagonal_collisions = reduce(lambda x, y: x + (y*(y-1))/2, left_diagonal_collisions + right_diagonal_collisions, 0) 
    return int(maxFitness - (horizontal_collisions + diagonal_collisions)) 

def probability(chromosome, fitness, maxFitness):
    return fitness(chromosome, maxFitness) / maxFitness

def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"
        
def reproduce(x, y): #doing cross_over between two chromosomes
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

def mutate(x):  #randomly changing the value of a random index of a chromosome
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x

def natural_selection(population, new_population, maxFitness):
    total_population = population + new_population
    new_total_population = sorted(total_population, key= lambda x: fitness(x, maxFitness))[::-1]
    return new_total_population[0:int(len(total_population)/2)]

def genetic_queen(population, fitness, maxFitness):
    mutation_probability = 0.03
    new_population = []
    father, mother, best_child = None, None, None
    probabilities = [probability(n, fitness, maxFitness) for n in population]
    for _ in range(len(population)):
        x = random_pick(population, probabilities) #best chromosome 1
        y = random_pick(population, probabilities) #best chromosome 2
        child = reproduce(x, y) #creating two new chromosomes from the best 2 chromosomes
        if random.random() < mutation_probability:
            child = mutate(child)
        # print_chromosome(child)
        new_population.append(child)
        if best_child is None:
            father, mother, best_child = x, y, child
        elif fitness(child, maxFitness) > fitness(best_child, maxFitness):
            father, mother, best_child = x, y, child
        if fitness(child, maxFitness) == maxFitness: break
    new_population = natural_selection(population, new_population, maxFitness)
    return new_population, [father, mother, best_child]

def print_chromosome(chrom):
    print("Chromosome = {},  Fitness = {}"
        .format(str(chrom), fitness(chrom)))

def solve(nq):
    start_time = time.time()
    maxFitness = (nq * (nq - 1)) / 2  # 8*7/2 = 28
    population = [random_chromosome(nq) for _ in range(100)]
    ranks = sorted(population, key= lambda x: fitness(x, maxFitness), reverse= True)
    initial = {'state':[{'x':y + 1,'y':z} for (y,z) in enumerate(ranks[0])], 'fitnessValue': fitness(ranks[0], maxFitness), 'parents':[]}
    generation = 1
    output = []
    output.append(initial)

    while not maxFitness in [fitness(chrom, maxFitness) for chrom in population]:
        print("=== Generation {} ===".format(generation), len(population))
        population, generation_output = genetic_queen(population, fitness, maxFitness)
        # print("")
        # ranks = sorted([(x, i) for (i, x) in enumerate(population)], key=lambda item: (fitness(item[0], maxFitness), item[1]), reverse=True)[:2]
        generation_output = list(map(lambda x: {'state':[{'x':y + 1,'y':z} for (y,z) in enumerate(x)], 'fitnessValue': fitness(x, maxFitness), 'parents': []}, generation_output))
        # print("Maximum Fitness = {}".format(max([fitness(n, maxFitness) for n in population])))
        generation_output[-1]['parents'] = generation_output[:2]
        output.append(generation_output[-1])
        generation += 1
    # [print(x) for x in output]
    # print(json.dumps({"generation": output, "time": time.time() - start_time}, indent=4, sort_keys=True))
    return output, time.time() - start_time
    # chrom_out = []
    # print("Solved in Generation {}!".format(generation - 1))
    # for chrom in population:
    #     if fitness(chrom) == maxFitness:
    #         print("");
    #         print("One of the solutions: ")
    #         chrom_out = chrom
    #         print_chromosome(chrom)

# if __name__ == "__main__":
#     solve(20)
    # nq = int(input("Enter Number of Queens: ")) #say N = 8
    # maxFitness = (nq*(nq-1))/2  # 8*7/2 = 28
    # population = [random_chromosome(nq) for _ in range(100)]
    #
    # generation = 1
    #
    # while not maxFitness in [fitness(chrom) for chrom in population]:
    #     print("=== Generation {} ===".format(generation), len(population))
    #     population = genetic_queen(population, fitness)
    #     print("")
    #     print("Maximum Fitness = {}".format(max([fitness(n) for n in population])))
    #     generation += 1
    # chrom_out = []
    # print("Solved in Generation {}!".format(generation-1))
    # for chrom in population:
    #     if fitness(chrom) == maxFitness:
    #         print("");
    #         print("One of the solutions: ")
    #         chrom_out = chrom
    #         print_chromosome(chrom)
            
    # board = []
    #
    # for x in range(nq):
    #     board.append(["x"] * nq)
    #
    # for i in range(nq):
    #     board[nq-chrom_out[i]][i]="Q"
    #
    #
    # def print_board(board):
    #     for row in board:
    #         print (" ".join(row))
    #
    # print()
    # print_board(board)
            
           
            
    

