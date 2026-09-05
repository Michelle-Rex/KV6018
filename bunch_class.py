import cylinder_class as cyl
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as PltCircle
import container_instances as prob

class Bunch:
    #manages the collection of cylinders and the placement aglorithms
    #needs argument "instance: prob.Instance"
    def __init__(self, instance: prob.Instance):
        self.container = instance.container
        self.all_placed = False
        self.cylinders = []

        for c in instance.cylinders:
            print(c)
            new_c = cyl.Cylinder(weight = c.weight, radius = c.diameter/2)
            self.cylinders.append(new_c)


    def reset(self):
        for cylinder in self.cylinders:
            cylinder.x = 0
            cylinder.y = 0
            cylinder.is_placed = False

    #create containing radius
    def get_containing_radius(self):
        if None in self.cylinders:
            raise Exception("Cylinder list empty")
        if self.all_placed == False:
            raise Exception("all cylinders not yet placed")
        else:
            all_containing_radii = []
            for c in self.cylinders:
                containing_radius = c.get_origin_distance() + c.radius
                all_containing_radii.append(containing_radius)
            return max(all_containing_radii)

    #check that all cylinders fit within the container
    #this won't work for rectangular containers, needs changing
    def check_fit(self, cyl):
        if cyl.get_origin_distance()+cyl.radius > self.container.width or cyl.get_origin_distance()+cyl.radius > self.container.depth:
           return False
        else:
            return True

     #find open points where the new cylinder can be placed         
    def find_open_points(self, new_cylinder): 
        open_points = []

        #get cylinders already placed
        placed = []
        for c in self.cylinders:
            if c.is_placed:
                placed.append(c)

        #place first cylinder at centre
        if len(placed) == 0: 
            #print("find_open_points works for placing first")
            open_points = [(0, 0, 0)]
            return open_points

        #Place second cyinder next to first 
        if len(placed) == 1:
            #print("find_open_points works for placing second") #debug statement
            c1 = placed[0]
            distance = c1.radius + new_cylinder.radius
            #print("distance =", distance)

            for angle in np.linspace(0, 2*np.pi, 36, endpoint = False):
                x = 0 + distance * np.cos(angle)
                y = 0 + distance * np.sin(angle)
                dist_from_origin = np.sqrt(x**2 + y**2) 
                #print(x, y) #debug statement

                if dist_from_origin + new_cylinder.radius > self.container.width or dist_from_origin + new_cylinder.radius > self.container.depth:
                    print("coordinates: ", x, y, "are outside the container") #debug statement
                else:
                    #print("cordinates: ", x, y, "are valid!") #debug statement
                    open_points.append((x, y, dist_from_origin))
            return open_points

        #for placing cylinders after the first 2
        #not working right now
        if len(placed) >= 2:
            #print("find open points works for 3+ cylinders") #debug statement 
            for i in range(0, len(placed)):
                for j in range(i+1, len(placed)):
                    #get last 2 cylinders placed
                    c1 = placed[i]
                    c2 = placed[j]

                    positions = self.find_tangent_positions(c1, c2, new_cylinder)
                    
                    if positions:
                        print("number of tangent positions returned = ", len(positions))
                        #print("tangent positions found") #debug statement #working
                        for x,y in positions: 
                            #print(x, y) #debug statement
                            temp_cyl = cyl.Cylinder(new_cylinder.radius, new_cylinder.weight)
                            temp_cyl.set_pos(x, y)

                            valid = self.check_fit(temp_cyl)
                             
                            for other in placed:
                                if other != c1 and other != c2:
                                    if temp_cyl.check_overlap(other):
                                        valid = False
                                        break
                                        

                        if valid:
                            dist_from_origin = np.sqrt(x**2 + y**2)
                            open_points.append((x, y, dist_from_origin))

                    else:
                        raise Exception("no tangent positions found")
        
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

    #place by radius 
    def sort_by_size(self):
        new_cylinders = self.cylinders
        new_cylinders.sort(key = lambda x: x.radius, reverse= True)
        return new_cylinders

    #place by weight
    def sort_by_weight(self):
        new_cylinders = self.cylinders
        new_cylinders.sort(key = lambda x: x.weight, reverse = True)
        return new_cylinders

    #randomize placement order
    def random_shuffle(self):
        random_order = self.cylinders
        return random.shuffle(random_order)

    #place all cylinders towards origin
    def place_towards_origin(self, cylinder_list):
        placed = 0
        for c in cylinder_list:
            open_points = self.find_open_points(c)
            print("cylinders placed = ", placed) #debug statement
            if open_points:
                print("number of open points is: ", len(open_points)) #debug statement
                best_position = min(open_points, key=lambda p: p[2])
                if best_position:
                    print("best found position is: ", best_position) #debug statement
                    c.set_pos(best_position[0], best_position[1])
                    placed = placed + 1
                else:
                    raise Exception("best position not found")
            else:
                raise Exception("No open points found")
        if placed == len(self.cylinders):
            self.all_placed = True  
            print(self.all_placed)     
          

    def place(self):
        #place in original order 
        #place closest to origin
        self.reset
        self.place_towards_origin(self.cylinders)
        if self.all_placed == True:
            self.draw(self.cylinders, "Original Order Place")
        else:
            raise Exception("not all circles placed")     


    def greedy_place_size(self):
        #place in order of largest to smallest by radius
        self.reset
        new_cylinders = self.sort_by_size()
        self.place_towards_origin(new_cylinders)
        self.draw(new_cylinders, "Greedy Place by Radius")
        return new_cylinders


    def random_place(self):
        #place in random order and position
        self.reset
        new_cylinders = self.random_shuffle
        self.place_towards_origin(new_cylinders)

    def draw(self, c_list, title):
        fig, ax = plt.subplots(figsize=(10, 10))
        
        #draw bounding circle
        containing_radius = self.get_containing_radius()
        bounding_circle = PltCircle((0, 0), containing_radius, fill=False, edgecolor='#F4BA02', linewidth=2, linestyle='--', label='Bounding Circle')
        ax.add_patch(bounding_circle)

        #draw cargo container
        rec_x = 0-(self.container.depth/2)
        rec_y = 0-(self.container.width/2)
        rec_container = plt.Rectangle((rec_x, rec_y), self.container.depth, self.container.width, fill=False, edgecolor='#F4BA02', linewidth=2, linestyle='--', label='Cargo Container')
        ax.add_patch(rec_container)

        for c in c_list:
            cylinder_patch = PltCircle((c.x, c.y), c.radius, fill=False, edgecolor='#99D9DD', linewidth=2)
            ax.add_patch(cylinder_patch)
            ax.plot(c.x, c.y, 'o', color='#99D9DD', markersize=6)
            ax.text(c.x, c.y, f'{int(c.radius)}', ha='center', va='center', color='#F7F8F9', fontsize=9)

        ax.plot(0, 0, 'x', color='#F4BA02', markersize=12, markeredgewidth=3, label='Origin')

        #set limits of grid to be a margin of 10 around the cargo container
        ax.set_aspect('equal')
        margin = 10
        ax.set_xlim((-self.container.depth/2) - margin, (self.container.depth/2) + margin)
        ax.set_ylim((-self.container.width/2) - margin, (self.container.width/2) + margin)

        ax.grid(True, alpha=0.3, color='#F7F8F9')
        ax.set_facecolor('#01364C')
        fig.patch.set_facecolor('#01364C')
        ax.tick_params(colors='#F7F8F9')
        for spine in ax.spines.values():
            spine.set_color('#F7F8F9')

        ax.set_title(f"{title}\nBounding Circle: {containing_radius:.2f}", color='#F7F8F9', fontsize=14, pad=20, weight='bold')
        ax.legend(loc='upper right', facecolor='#01364C', edgecolor='#F7F8F9', labelcolor='#F7F8F9', framealpha=0.9)

        ax.plot()
        plt.show()

        