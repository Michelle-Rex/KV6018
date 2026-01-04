from cylinder_class.py import Cylinder
import numpy as np

class Bunch:
    #manages the collection of cylinders and the placement aglorithms
    def __init__(self, radii, weight):
        self.cylinders = [
            Cylinder(r, w)
            for r in radii 
            for w in weight
        ]
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