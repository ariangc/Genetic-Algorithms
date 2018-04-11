import random
from NeuralNet import NeuralNet
from SnakeGame import SnakeGame

import numpy as np

ft = open("/dev/pts/21", "w")

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome

    def crossover(self, other):
        raise NotImplementedError

    def mutate(self):
        raise NotImplementedError

class Individual_snake(Individual):

    def __init__(self, chromosome=None):
        if(chromosome is not None):
            self.chromosome = chromosome
        else:
            self.chromosome = np.random.randint(0,2,size=(52,))

        self.fitness = -1
    
    def crossover_onepoint(self, other):
        c = random.randrange(len(self.chromosome))
        ind1 = Individual_snake(np.concatenate((self.chromosome[:c],other.chromosome[c:]), axis=0))
        ind2 = Individual_snake(np.concatenate((other.chromosome[:c],self.chromosome[c:]), axis=0))
        
        return [ind1,ind2]
    
    def mutate_random(self):
        #"Flip random quantity of bits of the chromosome"
        mutated_ind = Individual_snake(self.chromosome[:])
        n = random.randrange(len(mutated_ind.chromosome))
        for _ in range(n):
            x = random.randrange(len(mutated_ind.chromosome))
            if mutated_ind.chromosome[x] == 1:
                mutated_ind.chromosome[x] = 0
            else:
                mutated_ind.chromosome[x] = 1 
        
        return mutated_ind

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func,k,kwargs[k])
        return func
    return decorate

@static_vars(num_snake=0)
def fitness_snake(chromosome):
    fitness_snake.num_snake += 1
    weights = chromosome
    n = NeuralNet(weights)

    game = SnakeGame(gui = True)
    game.start()

    ft.write("Snake number {}\n".format(fitness_snake.num_snake))
    fitness = 0
    apples = 0
    prev = -100
    while(game.done == False):
        inputs = game.generate_input()
        action = n.getOutput(inputs, prev)
        apples = game.step(action)
        prev = action
        fitness-=1

    fitness += 200*apples
    if(game.done):
        fitness -= 100
    ft.write("Total fitness: {}\n".format(fitness))
    return fitness

def evaluate_population(population, fitness_fn):
    popsize = len(population)
    for i in range(popsize):
        if population[i].fitness == -1:
            population[i].fitness = fitness_fn(population[i].chromosome)

def select_parents_tournament(population):
    #We select randomly 3 individuals and choose the best
    randlist = []
    p1 = -1
    p2 = -1
    
    maxFitness = -1
    
    while (len(randlist) < 3):
        x = random.randrange(len(population))
        if(not(x in randlist)):
            randlist.append(x)
            if(population[x].fitness > maxFitness):
                p1 = x
                maxFitness = population[x].fitness
    
    randlist = []
    maxFitness = -1
    
    while (len(randlist) < 3):
        x = random.randrange(len(population))
        if(not(x in randlist) and x != p1):
            randlist.append(x)
            if(population[x].fitness > maxFitness):
                p2 = x
                maxFitness = population[x].fitness
    
    return [population[p1], population[p2]]

def select_survivors(population, offspring_population, numsurvivors):
    next_population = []
    population.extend(offspring_population)
    isurvivors = sorted(range(len(population)), key=lambda i: population[i].fitness, reverse = True)[:numsurvivors]
    for i in range(numsurvivors): next_population.append(population[isurvivors[i]])
    return next_population

def genetic_algorithm(population, fitness_fn,  ngen=100, pmut=0.1):
    popsize = len(population)
    evaluate_population(population, fitness_fn)
    ibest = sorted(range(len(population)), key=lambda i:population[i].fitness, reverse=True)[:1]
    bestfitness = [population[ibest[0]].fitness]
    
    ft.write("Poblacion incial, best_fitness = {}\n".format(population[ibest[0]].fitness))
    
    for g in range(ngen):
        mating_pool = []
        for i in range(popsize//2): mating_pool.append(select_parents_tournament(population))
        
        offspring_population = []
        
        for i in range(len(mating_pool)):
            offspring_population.extend(mating_pool[i][0].crossover_onepoint(mating_pool[i][1]))
            
        for i in range(len(offspring_population)):
            offspring_population[i] = offspring_population[i].mutate_random()
        
        evaluate_population(offspring_population,fitness_fn)
        
        population = select_survivors(population, offspring_population, popsize)
        
        ibest = sorted(range(len(population)), key=lambda i: population[i].fitness, reverse=True)[:1]
        bestfitness.append(population[ibest[0]].fitness)
        ft.write("Generacion {}, best_fitness = {}\n".format(g, population[ibest[0]].fitness))
    
    return population[ibest[0]], bestfitness

def genetic_search_snake(fitness_fn, popsize=10, ngen=100, pmut=0.1):
    population = []
    for i in range(popsize):
        population.append(Individual_snake())
    
    return genetic_algorithm(population, fitness_fn, ngen, pmut)

if __name__ == "__main__":
    genetic_search_snake(fitness_snake, 10,100,1)