import random
import math
import matplotlib.pyplot as plt

# from jarvis_march import jarvis_march

class DataGeneration:
    def __init__(self, x_range, y_range):
        self.points = []
        self.hull = []
        self.x_range = x_range
        self.y_range = y_range

    def generate_points(self, n, h=0):
        if h == 0:
            self.random_points(n)
        elif h >= 3:
            self.hull_points(n, h)
        else:
            raise ValueError("h must be greater than 3")
        return self.points

    def random_points(self, n):
        for i in range(n):
            x = random.randint(self.x_range[0], self.x_range[1])
            y = random.randint(self.y_range[0], self.y_range[1])
            self.points.append((x, y))

    def circle_points(self, n):
        x_middle = (self.x_range[1] - self.x_range[0]) / 2
        y_middle = (self.y_range[1] - self.y_range[0]) / 2
        radius = min(x_middle, y_middle)
        for i in range(n):
            angle = math.pi * 2 / n * i
            x = x_middle + radius * math.sin(angle)
            y = y_middle + radius * math.cos(angle)
            self.points.append((int(x), int(y)))

    def hull_points(self, n, h):
        self.circle_points(h)
        self.hull = self.points.copy()
        while len(self.points) < n:
            # swap these around depending on if we choose to use 
            # random points in a box or within the whole convex hull
            point = self.generate_random_points_in_box()
            # point = self.generate_points_inside_hull()
            self.points.append(point)

    def small_area_in_hull(self):
        middle = (self.x_range[1] - self.x_range[0]) / 2
        half_length = 5000
        return (middle - half_length, middle + half_length)
    
    def generate_random_points_in_box(self):
        length = self.small_area_in_hull()
        x = random.randint(length[0], length[1])
        y = random.randint(length[0], length[1])
        return (x,y)

    def generate_points_inside_hull(self):
        while True:
            x = random.randint(self.x_range[0], self.x_range[1])
            y = random.randint(self.y_range[0], self.y_range[1])
            point = (x, y)
            if self.is_inside_hull(point):
                return point

    def is_inside_hull(self, point):
        inside = False
        p1 = self.hull[0]
        for i in range(len(self.hull) + 1):
            p2 = self.hull[i % len(self.hull)]
            if min(p1[1], p2[1]) < point[1] <= max(p1[1], p2[1]) and point[0] <= max(p1[0], p2[0]):
                if p1[1] != p2[1]:
                    x_intercept = (point[1] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
                if point[0] <= x_intercept:
                    inside = not inside
            p1 = p2
        return inside

# generator = DataGeneration((0, 1000), (0, 1000))
# points = generator.generate_points(1000000, 20)
# hull = jarvis_march(points)
# plt.scatter(*zip(*points), color='black')
# hull.append(hull[0])
# xs, ys = zip(*hull)
# plt.plot(xs, ys, 'red', lw=2)
# plt.show()