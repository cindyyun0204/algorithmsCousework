import random
import math


class DataGeneration:
    def __init__(self, n, h, x_range, y_range, random=False, circle=False, hull=False, collinear=False):
        self.points = []
        self.hull = []
        self.n = n
        self.h = h
        self.x_range = x_range
        self.y_range = y_range
        # x and y ranges are tuples (a,b) from a to b
        self.random = random
        self.circle = circle
        self.collinear = collinear
        self.hull = hull

    def random_points(self, n):
        for i in range(n):
            x = random.randint(self.x_range[0], self.x_range[1])
            y = random.randint(self.y_range[0], self.y_range[1])
            self.points.append((x, y))
        return self.points

    def circle_points(self, n):
        x_middle = (self.x_range[1] - self.x_range[0]) / 2
        y_middle = (self.y_range[1] - self.y_range[0]) / 2
        radius = min(x_middle, y_middle)
        for i in range(n):
            angle = math.pi * 2 / n * i
            x = x_middle + radius * math.sin(angle)
            y = y_middle + radius * math.cos(angle)
            self.points.append((int(x), int(y)))
        return self.points

    def collinear_points(self):
        # makes a triangle for now
        self.n -= 1  # remove a point to add one later to complete hull
        m = (self.y_range[1] - self.y_range[0]) / (self.x_range[1] - self.x_range[0])
        c = self.y_range[0] - m * self.x_range[0]
        for i in range(self.n):
            x = (self.x_range[1] - self.x_range[0]) / (self.n - 1) * i
            y = m * x + c
            self.points.append((x, y))
        self.points.append(
            (self.x_range[1], self.y_range[0]))  # added the bottom right corner arbitrarily to allow hull to form
        return self.points

    def duplicate_points(self):
        # is there even any point in duplicating the test points?
        return self.points.extend(self.points)

    def hull_points(self):
        # this is really messy but it works ig
        # idea is to make a "circle" with h points with the function
        # choose if you want to use random or circle points
        self.circle_points(self.h)
        # self.random_points(self.h)
        self.hull = self.points.copy()
        while len(self.points) < self.n:
            point = self.generate_points_inside_hull()
            self.points.append(point)
        return self.points

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
            # compare with the line between p1 and p2
            if min(p1[1], p2[1]) < point[1] <= max(p1[1], p2[1]) and point[0] <= max(p1[0], p2[0]):
                # check if point is between the highest and lowest point of the line
                # and if it's to the left of the line
                if p1[1] != p2[1]:
                    x_intercept = (point[1] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
                if point[0] <= x_intercept:  # check if it crosses or touches the x-intercept on the right
                    inside = not inside
            p1 = p2
        return inside

    def choose_data(self):
        if self.random:
            self.random_points(self.n)
        if self.circle:
            self.circle_points(self.n)
        if self.collinear:
            self.collinear_points()
        if self.hull:
            self.hull_points()
        return self.points

# p = DataGeneration(1000000, 7, (0, 32767), (0, 32767), hull=True)
# p.choose_data()