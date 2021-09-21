from GeneticAlgorithm import FirstFit,NextFit,BestFit,WorstFit,Item
import random
from imports import instance,instance_v2
from datetime import datetime

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
   

class MoveOperator:
    @staticmethod
    def apply(items, choices):
        """
        Applies the operator to the given items.
        :param items: The items to which the operator should be applied.
        :param choices: Items that the operator can inject into the items if necessary.
        :return: The list of items after the operator was applied.
        """
        return items


class Remove(MoveOperator):
    @staticmethod
    def apply(items, choices):
        """
        Removes one or more of the items from the items list. Guarantees that there will always be at least one item
        left in the list of items.
        :param items: The items to which the operator should be applied.
        :param choices: Items that the operator can inject into the items if necessary.
        :return: The list of items after the operator was applied.
        """
        num_removals = random.randrange(len(items))
        for _ in range(num_removals):
            to_remove = random.randrange(len(items))
            items = items[:to_remove] + items[to_remove + 1:]
        return items


class Add(MoveOperator):
    @staticmethod
    def apply(items, choices):
        """
        Adds one or more randomly picked items from the choices list to the list of items.
        :param items: The items to which the operator should be applied.
        :param choices: Items that the operator can inject into the items if necessary.
        :return: The list of items after the operator was applied.
        """
        num_inserts = random.randrange(len(items) + 1)
        for _ in range(num_inserts):
            to_insert = random.randrange(len(items))
            items = items[:to_insert] + random.choice(choices) + items[to_insert:]
        return items


class Change(MoveOperator):
    @staticmethod
    def apply(items, choices):
        """
        Changes one or more of the items in the item list to a randomly picked item in the choices list.
        :param items: The items to which the operator should be applied.
        :param choices: Items that the operator can inject into the items if necessary.
        :return: The list of items after the operator was applied.
        """
        num_changes = random.randrange(len(items)+1)
        items = list(items)
        for _ in range(num_changes):
            to_change = random.randrange(len(items))
            items[to_change] = random.choice(choices)
        return "".join(items)


class Swap(MoveOperator):
    @staticmethod
    def apply(items, choices):
        """
        Swaps one or more of the items with another one in the item list.
        :param items: The items to which the operator should be applied.
        :param choices: Items that the operator can inject into the items if necessary.
        :return: The list of items after the operator was applied.
        """
        num_swaps = random.randrange(len(items))
        items = list(items)
        for _ in range(num_swaps):
            idx1, idx2 = random.randrange(len(items)), random.randrange(len(items))
            items[idx1], items[idx2] = items[idx2], items[idx1]
        return "".join(items)


class TabuSearch:

    heuristic_map = {
        "f": FirstFit,
        "n": NextFit,
        "w": WorstFit,
        "b": BestFit,
    }
    movers = [Add, Change, Remove, Swap] 

    def __init__(self, capacity, items, MAX_COMBINATION_LENGTH=10, MAX_ITERATIONS=5000, MAX_NO_CHANGE = 1000):
        """
        Creates an instance that can run the tabu search algorithm.
        :param capacity: The capacity of a bin.
        :param items: The items that have to be packed in bins.
        """
        self.MAX_COMBINATION_LENGTH = MAX_COMBINATION_LENGTH
        self.MAX_ITERATIONS = MAX_ITERATIONS
        self.MAX_NO_CHANGE = MAX_NO_CHANGE
        self.bin_capacity = capacity
        self.items = items
        self.fitness = 0
        self.bins = [Bin(capacity)]
        self.tabu_list = set()
    # def get_Bins():
    #     return self.bins

    def run(self):
        """
        Runs the tabu search algorithm and returns the results at the end of the process.
        :return: (num_iterations, num_no_changes, chosen_combination)
        """
        combination = "".join(
            [random.choice(list(self.heuristic_map.keys())) for _ in range(random.randrange(self.MAX_COMBINATION_LENGTH) or 1)])
        self.bins = self.generate_solution(combination)
        self.fitness = sum(b.fitness() for b in self.bins) / len(self.bins)
        self.tabu_list.add(combination)
        current_iteration = 0
        num_no_change = 0
        while num_no_change < self.MAX_NO_CHANGE and current_iteration < self.MAX_ITERATIONS:
            print('while2',current_iteration)
            new_combination = self.apply_move_operator(combination)
            while len(new_combination) > self.MAX_COMBINATION_LENGTH :
                new_combination = self.apply_move_operator(new_combination)
                print('while2')
            if new_combination not in self.tabu_list:
                self.tabu_list.add(new_combination)
                solution = self.generate_solution(new_combination)
                fitness = sum(b.fitness() for b in solution) / len(solution)
                if fitness > self.fitness:
                    self.bins = solution
                    self.fitness = fitness
                    num_no_change = 0
                    combination = new_combination
            current_iteration += 1
            num_no_change += 1
        return current_iteration, num_no_change, combination
    def run2(self,AGsol):
        """
        Runs the tabu search algorithm and returns the results at the end of the process.
        :return: (num_iterations, num_no_changes, chosen_combination)
        """
        combination = AGsol.best_solution.pattern
        self.bins =self.generate_solution(combination) 
        self.fitness = AGsol.best_solution.fitness
        self.tabu_list.add(combination)
        current_iteration = 0
        num_no_change = 0
        while num_no_change < self.MAX_NO_CHANGE and current_iteration < self.MAX_ITERATIONS:
            new_combination = self.apply_move_operator(combination)
            while len(new_combination) > self.MAX_COMBINATION_LENGTH :
                new_combination = self.apply_move_operator(new_combination)
            if new_combination not in self.tabu_list:
                self.tabu_list.add(new_combination)
                solution = self.generate_solution(new_combination)
                fitness = sum(b.fitness() for b in solution) / len(solution)
                if fitness > self.fitness:
                    self.bins = solution
                    self.fitness = fitness
                    num_no_change = 0
                    combination = new_combination
                current_iteration += 1
            else : 
                current_iteration += 1
                num_no_change += 1
        return current_iteration, num_no_change, combination
    def run3(self,chromosome):
        """
        Runs the tabu search algorithm and returns the results at the end of the process.
        :return: (num_iterations, num_no_changes, chosen_combination)
        """
        combination = chromosome.pattern
        self.bins =self.generate_solution(combination) 
        self.fitness = chromosome.fitness
        self.tabu_list.add(combination)
        current_iteration = 0
        num_no_change = 0
        while num_no_change < self.MAX_NO_CHANGE and current_iteration < self.MAX_ITERATIONS:
            new_combination = self.apply_move_operator(combination)
            while len(new_combination) > self.MAX_COMBINATION_LENGTH :
                new_combination = self.apply_move_operator(new_combination)
            if new_combination not in self.tabu_list:
                self.tabu_list.add(new_combination)
                solution = self.generate_solution(new_combination)
                fitness = sum(b.fitness() for b in solution) / len(solution)
                if fitness > self.fitness:
                    self.bins = solution
                    self.fitness = fitness
                    num_no_change = 0
                    combination = new_combination
                current_iteration += 1
            else : 
                current_iteration += 1
                num_no_change += 1
        return current_iteration, num_no_change, combination

    def generate_solution(self, pattern):
        """
        Generates a candidate solution based on the pattern given.
        :param pattern: A pattern indicating the order in which heuristics need to be applied to get the solution.
        :return: A list of bins to serve as a solution.
        """
        solution = [Bin(self.bin_capacity)]
        pattern_length = len(pattern)
        for idx, item in enumerate(self.items):
            h = pattern[idx % pattern_length]
            solution = self.heuristic_map[h].apply(item, solution)
        return solution

    def apply_move_operator(self, pattern):
        """
        Applies a random move operator to the given pattern.
        :param pattern: The pattern to apply the move operator to.
        :return: The pattern after the move operator has been applied.
        """
        return random.choice(self.movers).apply(pattern, list(self.heuristic_map.keys()))

def TS( capacity, items, MAX_COMBINATION_LENGTH=10, MAX_ITERATIONS=5000, MAX_NO_CHANGE = 1000):
    objets = [Item(size=i) for i in items]
    thing = TabuSearch(capacity, objets)
    #print(thing.tabu_list)
    start_time = datetime.now()
    total_iterations, stagnation, combination = thing.run()
    execution_time = datetime.now() - start_time     
    beConf = [[item.getSize(),i] for i,bin in enumerate(thing.bins) for item in bin.getItems()]
    #print(len(thing.bins), beConf)
    return len(thing.bins), beConf,execution_time.total_seconds()


# capacity,items = instance_v2('instances/Moyenne/T_Petite_100/N2W4B1R0.txt')
# TS(capacity,items)