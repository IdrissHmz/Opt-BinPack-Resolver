# coding=utf-8
#from heuristics import BestFit, FirstFit, NextFit, WorstFit
import random
from random import shuffle
from datetime import datetime
from imports import instance
import time

class Item:
    def __init__(self,size):
        self.size = size
    def getSize(self):
        return self.size

class Bin:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def getItems(self):
        return self.items

    def add_item(self, new_item):
        """
        Attempts to add an item to the list of items in this bin.
        :param new_item: The item to add.
        :return: True if the item was added successfully, False otherwise.
        """
        if self.can_add_item(new_item):
            self.items.append(new_item)
            return True
        return False

    def can_add_item(self, new_item):
        """
        Determines whether the specified item can be added to the bin's list of items.
        :param new_item: The item to check.
        :return: True if the item can be added, False otherwise.
        """
        return new_item.size <= self.open_space()

    def filled_space(self):
        """
        Gets the amount of space currently in use by items in the bin.
        :return: The amount of space currently in use.
        """
        return sum(item.size for item in self.items)

    def open_space(self):
        """
        Gets the amount of space that is still available in this bin.
        :return: The amount of space that this bin has left.
        """
        return self.capacity - self.filled_space()

    def fitness(self):
        """
        Returns a value that can be used to indicate the fitness of this bin when calculating the fitness of a solution.
        :return: (fullness / capacity) ^ 2
        """
        return (self.filled_space() / self.capacity) ** 2
   




class Heuristic:
    @staticmethod
    def apply(item, bins):
        """
        Applies the heuristic to the given bins. This has to be overridden by subclasses.
        :param item: The item to add.
        :param bins: The list of bins to choose from.
        :return: The lists of bins after insertion.
        """
        return bins


class FirstFit(Heuristic):
    @staticmethod
    def apply(item, bins):
        """
        Adds the item to the very first bin that it can fit it.
        :param item: The item to add.
        :param bins: The bins to choose from.
        :return: The list of bins after the insertion.
        """
        b = next((b for b in bins if b.can_add_item(item)), None)
        if not b:
            b = Bin(bins[0].capacity)
            bins.append(b)
        b.add_item(item)
        return bins


class BestFit(Heuristic):
    @staticmethod
    def apply(item, bins):
        """
        Adds the item to the bin for which the least amount of open space would be available after insertion.
        :param item: The item to add.
        :param bins: The bins to choose from.
        :return: The list of bins after the insertion.
        """
        valid_bins = (b for b in bins if b.can_add_item(item))
        # Note that this method is exactly the same as for the BestFit heuristic except for the following line.
        sorted_bins = sorted(valid_bins, key=lambda x: x.filled_space(), reverse=True)
        if sorted_bins:
            b = sorted_bins[0]
        else:
            b = Bin(bins[0].capacity)
            bins.append(b)
        b.add_item(item)
        return bins


class NextFit(Heuristic):
    @staticmethod
    def apply(item, bins):
        """
        Adds the item to the next available bin after the last insertion.
        :param item: The item to add.
        :param bins: The bins to choose from.
        :return: The list of bins after insertion.
        """
        b = bins[-1]
        if not b.add_item(item):
            b = Bin(bins[0].capacity)
            bins.append(b)
            b.add_item(item)
        return bins


class WorstFit(Heuristic):
    @staticmethod
    def apply(item, bins):
        """
        Adds the item to the bin for which the most amount of open space would be available after insertion.
        :param item: The item to add.
        :param bins: The bins to choose from.
        :return: The list of bins after insertion.
        """
        valid_bins = (b for b in bins if b.can_add_item(item))
        sorted_bins = sorted(valid_bins, key=lambda x: x.filled_space())
        if sorted_bins:
            b = sorted_bins[0]
        else:
            b = Bin(bins[0].capacity)
            bins.append(b)
        b.add_item(item)
        return bins

class FirstFitDec (Heuristic):
    @staticmethod
    def apply(item, bins):
	    """ Returns list of bins with input items inside. """
	    
	    return(FirstFit.apply(item, bins))

class NextFitDec (Heuristic):
    @staticmethod
    def apply(item, bins):
	    """ Returns list of bins with input items inside. """
	    
	    return(NextFit.apply(item, bins))

class BestFitDec (Heuristic):
    @staticmethod
    def apply(item, bins):
	    """ Returns list of bins with input items inside. """
	    
	    return(BestFit.apply(item, bins))

class WorstFitDec (Heuristic):
    @staticmethod
    def apply(item, bins):
	    """ Returns list of bins with input items inside. """
	    
	    return(WorstFit.apply(item, bins))





class GeneticAlgorithm:

    def __init__(self, capacity, items,POPULATION_SIZE = 50,MAX_GENERATIONS = 250,MAX_NO_CHANGE = 50 ,TOURNAMENT_SIZE = 20 ,MUTATION_RATE = 0.3 ,CROSSOVER_RATE = 0.6, population=None):
        """
        Creer une instance pour l'algorithme genetique.
        les paramètres de l'algorithme génétique:
        POPULATION_SIZE: la taille de la population
        """
        self.POPULATION_SIZE = POPULATION_SIZE
        self.MAX_GENERATIONS = MAX_GENERATIONS
        self.MAX_NO_CHANGE = MAX_NO_CHANGE
        self.TOURNAMENT_SIZE = TOURNAMENT_SIZE
        self.MUTATION_RATE = MUTATION_RATE
        self.CROSSOVER_RATE = CROSSOVER_RATE
        self.items = items
        self.best_solution = None
        if population == None:
            self.population = [Chromosome(capacity) for _ in range(self.POPULATION_SIZE)]
            self.update_individuals(self.population)
        else:
            self.population = population
            self.update_individuals(self.population)

    def run(self):
        """
        Runs the genetic algorithm and returns the results at the end of the process.
        :return: (num_iterations, num_no_changes)
        """
        current_iteration = 0
        num_no_change = 0
        while num_no_change < self.MAX_NO_CHANGE and current_iteration < self.MAX_GENERATIONS:
            new_generation = []
            while len(new_generation) < self.POPULATION_SIZE:
                # Select parents
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                # Apply genetic operators
                child1, child2 = self.crossover(parent1, parent2)
                child1, child2 = self.mutate(child1), self.mutate(child2)
                # Update the fitness values of the offspring to determine whether they should be added
                self.update_individuals([child1, child2])
                sorted_list = sorted([parent1, parent2, child1, child2], key=lambda x: x.fitness, reverse=True)
                # Add to new generation the two best chromosomes of the combined parents and offspring
                new_generation.append(sorted_list[0])
                new_generation.append(sorted_list[1])
            self.population = new_generation
            prev_best = self.best_solution
            # Evaluate fitness values
            self.best_solution,best_conf = self.update_individuals(self.population)
            # Check if any improvement has happened.
            if not prev_best or prev_best.fitness == self.best_solution.fitness:
                num_no_change += 1
            else:
                num_no_change = 0
            current_iteration += 1
        return current_iteration, num_no_change,best_conf

    def mutate(self, chromosome):
        """
        Attempts to mutate the chromosome by replacing a random heuristic in the chromosome by a generated pattern.
        :param chromosome: The chromosome to mutate.
        :return: The mutated chromosome.
        """
        pattern = list(chromosome.pattern)
        if random.random() < self.MUTATION_RATE:
            mutation_point = random.randrange(len(pattern))
            pattern[mutation_point] = Chromosome.generate_pattern()
        return Chromosome(chromosome.bin_capacity, "".join(pattern))

    def crossover(self, parent1, parent2):
        """
        Attempt to perform crossover between two chromosomes.
        :param parent1: The first parent.
        :param parent2: The second parent.
        :return: The two individuals after crossover has been performed.
        """
        pattern1, pattern2 = parent1.pattern, parent2.pattern
        if random.random() < self.CROSSOVER_RATE:
            point1, point2 = random.randrange(len(pattern1)), random.randrange(len(pattern2))
            substr1, substr2 = pattern1[point1:], pattern2[point2:]
            pattern1, pattern2 = "".join((pattern1[:point1], substr2)), "".join((pattern2[:point2], substr1))
        return Chromosome(parent1.bin_capacity, pattern1), Chromosome(parent2.bin_capacity, pattern2)


    def update_individuals(self, individuals):
        """
        Update the fitness values of all the chromosomes in the population.
        """
        for individual in individuals:
            solution = individual.generate_solution(self.items)
            individual.num_bins = len(solution)
            individual.fitness = sum(b.fitness() for b in solution) / len(solution)
        return max(self.population, key=lambda x: x.fitness),solution

    def select_parent(self):
        """
        Selects a parent from the current population by applying tournament selection.
        :return: The selected parent.
        """
        candidate = random.choice(self.population)
        for _ in range(self.TOURNAMENT_SIZE - 1):
            opponent = random.choice(self.population)
            if opponent.fitness > candidate.fitness:
                candidate = opponent
        return candidate


class Chromosome:
    MAX_COMBINATION_LENGTH = 10
    heuristic_map = {
        "f": FirstFit,
        "n": NextFit,
        "w": WorstFit,
        "b": BestFit,
    }

    def __init__(self, capacity, pattern=None):
        self.bin_capacity = capacity
        self.fitness = 0
        self.num_bins = 0
        self.pattern = pattern or self.generate_pattern()

    @staticmethod
    def generate_pattern():
        """
        Generates a random pattern.
        :return: The generated pattern string.
        """
        return "".join(
            [random.choice(list(Chromosome.heuristic_map.keys())) for _ in range(random.randrange(Chromosome.MAX_COMBINATION_LENGTH) or 1)])

    def generate_solution(self, items):
        """
        Generates a candidate solution based on the pattern given.
        :param items: The items that need to be used when generating a solution.
        :return: A list of bins to serve as a solution.
        """
        solution = [Bin(self.bin_capacity)]
        pattern_length = len(self.pattern)
        for idx, item in enumerate(items):
            h = self.pattern[idx % pattern_length]
            solution = self.heuristic_map[h].apply(item, solution)
        return solution
    
def AG(items,capacite,POPULATION_SIZE = 50,MAX_GENERATIONS = 250,MAX_NO_CHANGE = 5 ,TOURNAMENT_SIZE = 5 ,MUTATION_RATE = 0.3 ,CROSSOVER_RATE = 0.6, population=None):

    temps_Debut_exec = datetime.now()

    objets = [Item(size=i) for i in items]
    solution = GeneticAlgorithm(capacite, objets,POPULATION_SIZE = 50,MAX_GENERATIONS = 250,MAX_NO_CHANGE = 50 ,TOURNAMENT_SIZE = 20 ,MUTATION_RATE = 0.3 ,CROSSOVER_RATE = 0.6, population=None)

    total_iter, x, best_conf = solution.run()
    temps_apres_exec= datetime.now()
    temps_exec = (temps_apres_exec - temps_Debut_exec).total_seconds()

    beConf = [[item.getSize(),i] for i,bin in enumerate(best_conf) for item in bin.getItems()]
    
    
    return solution.best_solution.num_bins, beConf, temps_exec





#meta,items = instance('N1C1W1_A.txt')
# print( AG(items, int(meta[0])))    