#from cylinder_class.py import Cylinder
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

class Bunch:
    #manages the collection of cylinders and the placement aglorithms
    def __init__(self, radii, weight):
        self.cylinders = [Cylinder(radii[i], weight[i]) for i in (0, len(radii)-1)]
        self.radii = radii
        self.weight = weight

    def reset(self):
        for cylinder in self.cylinders:
            cylinder.x = 0
            cylinder.y = 0
            cylinder.is_placed = False

    def get_containing_radius(self):
        if None in self.cylinders:
            return 0
        for cylinder in self.cylinders:
            return max(c.containing_radius for c in self.cylinders)
        #not sure if i need this

    def find_open_points(self, new_cylinder): #find open points where the new cylinder can be placed 
        open_points = []
        placed = [c for c in self.cylinders if c.placed]

        if len(placed) == 0: 
            #place first at origin
            return [(0,0)]
        
        if len(placed) == 1:
            #place second cylinder next to the first, gived different angles to try
            c1 = placed[0]
            distance = c1.radius + new_cylinder.radius
            for angle in np.linspace(0, 2*np.pi, 36, endpoint = False):
                x = c1.x + distance * np.cos(angle)
                y = c1.y + distance * np.sin(angle)
                #dist_from_origin = np.sqrt(x**2 + y**2)   DO I NEED THIS?? WE'LL FIND OUT IN THE NEXT EPISODE
                open_points.append((x,y))

        return open_points

    def get_centre_grav(self): #get the  centre of gravity of all the circles
        pass

    def ordered_place(self):
        for c in self.cylinders:
            pass

#testing

test_bunch = Bunch([10, 6], [10, 8])
for b in test_bunch.cylinders:
    print(b.weight)