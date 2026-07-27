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

    def find_open_points(self, new_cylinder): 
        #find open points where the new cylinder can be placed 
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
         #returns positions which tangent the previous 2 cylinders 
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
        return self.cylinders.sort(key = self.size_sort_key)
    
    def sort_by_weight(self):
        return self.cylinders.sort(key = self.weight_sort_key)

    def random_shuffle(self):
        random_order = self.cylinders
        return random.shuffle(random_order)

    def place_towards_origin(self, cylinder_order):
        for c in cylinder_order:
            open_points = self.find_open_points(c)
          
            if open_points:
                best_position = min(open_points, key=lambda p: p[2])
                c.set_pos(best_position[0], best_position[1])         
          

    def ordered_place(self):
        #place in original order 
        #place closest to origin
        self.reset
        self.place_towards_origin(self.cylinders)     

    def greedy_place_size(self):
        #place in order of largest to smallest by radius
        self.reset
        new_cylinders = self.sort_by_size
        self.place_towards_origin(new_cylinders)

    def random_place(self):
        #place in random order and position
        self.reset
        new_cylinders = self.random_shuffle
        self.place_towards_origin(new_cylinders)

    def draw(self, title = "Cylinder Placement", show_open_points = False):
        #set up the graph
        fig, ax = plt.subplots(figsize=(10, 10))
        containing_radius = self.get_containing_radius()
        container = plt.Rectangle((0,0), width = self.rec_width, height = self.rec_len, fill = False, edgecolour = "#0052cc", linewidth = 2, label = "Cargo Container")
        ax.add_patch(container)
        ax.set_aspect('equal')

        ax.plot(0,0, 'x', color = "#0052cc", markersize = 12, markeredgewidth = 3, label = "Origin")
        margin = 10
        ax.set_xlim = self.rec_width + margin
        ax.set_ylim = self.rec_len + margin
        ax.grid(True, alpha = 0.3, color = "w")
        ax.set_facecolor("#01364C")
        fig.patch.set_facecolor("#01364C")
        ax.tick_params(colors = "w")
        for spine in ax.spines.values():
            spine.set_color("w")
        
        ax.set_title(f"{title}\nContaining Radius: {containing_radius:.2f}", 
                    color='w', fontsize=14, pad=20, weight='bold')
        ax.legend(loc='upper right', facecolor='#01364C', edgecolor='#F7F8F9', 
                 labelcolor='#F7F8F9', framealpha=0.9)
        
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
                cylinder_patch = plt.Circle((cylinder.x, cylinder.y), cylinder.radius,fill=False, edgecolor= "#66ccff", linewidth=2)
                ax.add_patch(cylinder_patch)
                ax.plot(cylinder.x, cylinder.y, 'o', color = "#66ccff", markersize = 6)
                ax.text(cylinder.x, cylinder.y, f'{int(cylinder.radius)}', ha='center', va='center', color='#F7F8F9', fontsize=9)

        
#testing