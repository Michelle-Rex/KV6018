import cylinder_class as cyl
import numpy as np
import random
import matplotlib.pyplot as plt

class Bunch:
    #manages the collection of cylinders and the placement aglorithms
    def __init__(self, radii, weight, rec_len, rec_width):
        self.cylinders = [cyl.Cylinder(radii[i], weight[i]) for i in (0, len(radii)-1)]
        self.radii = radii
        self.weight = weight
        self.rec_len = rec_len
        self.rec_width = rec_width

    def reset(self):
        for cylinder in self.cylinders:
            cylinder.x = 0
            cylinder.y = 0
            cylinder.is_placed = False

    def get_containing_radius(self):
        if None in self.cylinders:
            return 0
        for c in self.cylinders:
            return max(c.containing_radius for c in self.cylinders)
    
    def check_fit(self):
        if self.get_containing_radius()*2 > self.rec_len or self.get_containing_radius()*2 > self.rec_width:
            return "invalid solution: does not fit within container"

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
                dist_from_origin = np.sqrt(x**2 + y**2)  
                if not dist_from_origin + new_cylinder.radius > self.rec_len/2 and not dist_from_origin + new_cylinder.radius > self.rec_width/2:
                    #should only add points which ensure the cylinder fits within the rectangle
                    open_points.append((x,y))
            return open_points
    
        for i in (len(placed)):
            for j in range(i+1, len(placed)):
                c1 = placed[i]
                c2 = placed [j]

                positions = self.find_tangent_positions(c1, c2, new_cylinder)
                for x,y in positions: 
                    temp_cyl = cyl.Cylinder(new_cylinder.radius, new_cylinder.weight)
                    temp_cyl.set_pos(x, y)

                    valid = True

                    for other in placed:
                        if other != c1 and other != c2:
                            if temp_cyl.check_overlap(other):
                                valid = False
                                break

                    if valid:
                        dist_from_origin = np.sqrt(x**2 + y**2)
                        open_points.append((x, y, dist_from_origin))

        return open_points

    def find_tangent_positions(self, c1, c2, new_cylinder):
         #find where the new circle can be placed to tangent with the previous 2 (uses circle-circle intersection --not entirely sure how the geometry works)
        r1 = c1.radius + new_cylinder.radius
        r2 = c2.radius + new_cylinder.radius
        d = c1.distance_to_other(c2)

        if d > r1 + r2 or d < abs(r1 - r2) or d ==0:
            return []
        
        a = (r1**2 - r2**2 +d**2)/ (2*d)
        h = np.sqrt(max(0, r1**2 - a**2))

        px = c1.x + a * (c2.x - c1.x) / d
        py = c1.y + a * (c2.y - c1.y) / d

        positions = []

        if h > 0.01:
            positions.append((
                px + h * (c2.y - c1.y) / d,
                py - h * (c2.x - c1.x) / d
            ))
            positions.append((
                px - h * (c2.y - c1.y) / d,
                py + h * (c2.x - c1.x) / d
            ))
        else:
            positions.append((px, py))

        return positions
        


    def get_centre_grav(self): #get the  centre of gravity of all the circles
        pass
    
    def weight_sort_key(e):
        return e.weight

    def size_sort_key(e):
        return e.radii
    
    def sort_by_size(self):
        self.cylinders.sort(key = self.size_sort_key)
    
    def sort_by_weight(self):
        self.cylinders.sort(key = self.weight_sort_key)

    def random_shuffle(self):
        random.shuffle(self.cylinders)

    def ordered_place(self, type):
        #place first cylinder in the centre
        for c in self.cylinders:
            open_points = self.find_open_points(c)

            if open_points:
                pass

    def draw(self, title = "Cylinder Placement", show_open_points = False):
        #set up
        fig, ax = plt.subplots(figsize=(10, 10))
        containing_radius = self.get_containing_radius()
        container = plt.Rectangle((0,0), width = self.rec_width, height = self.rec_len, fill = False, edgecolour = "black", linewidth = 2, label = "Cargo Container")
        
        ax.add_patch(container)

        #I'm not entirely sure on how this if statement resolves, as far as I can tell it's checking 
        if show_open_points and len([c for c in self.cylinders if c.is_placed]) < len(self.cylinders):
            next_cylinder = [c for c in self.cylinders if not c.is_placed][0]
            open_points = self.find_open_points(next_cylinder)

            if open_points:
                xs, ys = zip(*[(p[0], p[1]) for p in open_points])
                ax.scatter(xs, ys, c= "lime", s=30, alpha = 0.5, zorder = 5, label = "Open Points")

        for cylinder in self.cylinders:
            if cylinder.is_placed():
                cylinder_patch = plt.Circle((cylinder.x, cylinder.y), cylinder.radius,
                                        fill=False, edgecolor= "#66ccff", linewidth=2)
                ax.add_patch(cylinder_patch)
    

#testing