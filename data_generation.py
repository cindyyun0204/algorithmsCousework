import random
import math

class DataGeneration:
    def __init__(self, num_points, x_range, y_range):
        self.points = []
        self.num_points = num_points
        self.x_range = x_range 
        self.y_range = y_range
        # x and y ranges are tuples (a,b) from a to b
    
    def random_points(self):
        for i in range(self.num_points):
            self.points.append((random.randint(self.x_range[0], self.x_range[1]), random.randint(self.y_range[0], self.y_range[1])))
        return self.points
    
    def circle_points(self):
        x_middle = (self.x_range[1] - self.x_range[0]) / 2
        y_middle = (self.y_range[1] - self.y_range[0]) / 2
        radius = min(x_middle, y_middle)
        for i in range(self.num_points):
            angle = math.pi * 2 / self.num_points * i
            x = x_middle + radius * math.sin(angle)
            y = y_middle + radius * math.cos(angle)
            self.points.append((int(x), int(y)))
        return self.points
    
    def collinear_points(self): # makes a triangle for now
        m = (self.y_range[1] - self.y_range[0]) / (self.x_range[1] - self.x_range[0])
        c = self.y_range[0] - m * self.x_range[0]
        for i in range(self.num_points):
            x = (self.x_range[1] - self.x_range[0]) / self.num_points * i
            y = m * x + c
            self.points.append((x, y))
        self.points.append((self.x_range[1], self.y_range[0])) # added the bottom right corner arbitrarily to allow hull to form
        return self.points

    def duplicate_points(self):
        pass

    def concave_hull(self):
        pass

p = DataGeneration(4, (0, 100), (0, 100))
# print(p.random_points())
# print(p.circle_points())
# print(p.collinear_points())