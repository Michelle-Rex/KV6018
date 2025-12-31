import cylinder_class.py as cyl

class Bunch:
    def __init__(self, radii, weight):
        self.cylinders = [
            cyl.Cylinder(r, w)
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
            return max(cyl.c.containing_radius for c in self.cylinders)