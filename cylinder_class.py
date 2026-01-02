import numpy as np

class Cylinder:
    def __init__(self, radius, weight):
        self.radius = radius
        self.weight = weight
        self.x = 0
        self.y = 0
        self.is_placed = False

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.is_placed = True
    
    def get_origin_distance(self):
        return np.sqrt(self.x**2 + self.y**2)
    
    def containing_radius(self):
        return self.get_origin_distance + self.radius
    
    def distance_to_other(self, other):
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def check_overlap(self, other):
        distance = self.distance_to_other(other)
        return distance < (self.radius + other.radius + 0.01)
    