import bunch_class as bunch
import cylinder_class as cyl
import population_class as pop
import numpy as np
import matplotlib.pyplot as plt

#testing
container_l = 100
container_w = 200
cylinders_radii = [2, 5, 3, 6, 8]
cylinders_weight = [2, 3, 6, 7, 8]

test_bunch = bunch.Bunch(cylinders_radii, cylinders_weight, container_l, container_w)
test_bunch.reset()
test_bunch.ordered_place()