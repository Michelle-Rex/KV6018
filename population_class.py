import container_instances as prob
import numpy as np
import matplotlib.pyplot as plt

class Population:
    def __init__(self, instance: prob.Instance):
        self.population = [] #list of generates solutions (each list is a list of cylinders, the order is the genome)
        self.pop_size = 10
        self.max_gens = 5
        self.gen_count = 0
        self.mutation_rate = 0.2
        self.tournament_pool = 3
        self.best_solution = None
        self.best_solution_fitness = 0

    def tournament():
        pass

    def find_best_solution():
        pass

    def get_fitness():
        pass

