import bunch_class as bunch
import cylinder_class as cyl
import population_class as pop
import numpy as np
import matplotlib.pyplot as plt
import container_instances as prob

def printSolution(solution: list):
    for c in solution:
        print(c.radius*2) #to get diameter

problems = prob.create_basic_instances()
test_bunch = bunch.Bunch(problems[0])
#test_bunch.place()
solution = test_bunch.greedy_place_size()