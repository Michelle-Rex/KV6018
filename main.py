import bunch_class as bunch
import cylinder_class as cyl
import population_class as pop
import numpy as np
import matplotlib.pyplot as plt

#testing
container_l = 10
container_w = 20
cylinders_radii = [2, 5, 3, 6, 8]
cylinders_weight = [2, 3, 6, 7, 8]

test_bunch = bunch.Bunch(cylinders_radii, cylinders_weight, container_l, container_w)
print(len(test_bunch.cylinders))