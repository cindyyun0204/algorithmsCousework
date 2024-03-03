import random
import math
import matplotlib.pyplot as plt

class DataGeneration:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range

    def generate_random_convex_polygon(self, n):
        # Generate two lists of random X and Y coordinates within the range 1 to 10,000
        x_pool = [random.randint(0, 32767) for _ in range(n)]
        y_pool = [random.randint(0, 32767) for _ in range(n)]

        # Sort them
        x_pool.sort()
        y_pool.sort()

        # Isolate the extreme points
        min_x, max_x = x_pool[0], x_pool[-1]
        min_y, max_y = y_pool[0], y_pool[-1]

        # Divide the interior points into two chains & Extract the vector components
        x_vec, y_vec = [], []

        last_top, last_bot = min_x, min_x
        for x in x_pool[1:-1]:
            if random.choice([True, False]):
                x_vec.append(x - last_top)
                last_top = x
            else:
                x_vec.append(last_bot - x)
                last_bot = x
        x_vec += [max_x - last_top, last_bot - max_x]

        last_left, last_right = min_y, min_y
        for y in y_pool[1:-1]:
            if random.choice([True, False]):
                y_vec.append(y - last_left)
                last_left = y
            else:
                y_vec.append(last_right - y)
                last_right = y
        y_vec += [max_y - last_left, last_right - max_y]

        # Randomly pair up the X- and Y-components
        random.shuffle(y_vec)

        # Combine the paired up components into vectors
        vec = [(x_vec[i], y_vec[i]) for i in range(n)]

        # Sort the vectors by angle
        vec.sort(key=lambda v: math.atan2(v[1], v[0]))

        # Lay them end-to-end
        x, y = 0, 0
        min_polygon_x, min_polygon_y = 0, 0
        points = []

        for vx, vy in vec:
            points.append((x, y))
            x += vx
            y += vy
            min_polygon_x = min(min_polygon_x, x)
            min_polygon_y = min(min_polygon_y, y)

        # Move the polygon to the original min and max coordinates
        x_shift = min_x - min_polygon_x
        y_shift = min_y - min_polygon_y
        points = [(int(p[0] + x_shift), int(p[1] + y_shift)) for p in points]
        return points

    def is_point_inside_polygon(self, x, y, polygon):
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def generate_points_inside_polygon(self, polygon, num_points):
        min_x = min(polygon, key=lambda t: t[0])[0]
        max_x = max(polygon, key=lambda t: t[0])[0]
        min_y = min(polygon, key=lambda t: t[1])[1]
        max_y = max(polygon, key=lambda t: t[1])[1]
        points_inside = []
        while len(points_inside) < num_points:
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            if self.is_point_inside_polygon(x, y, polygon):
                points_inside.append((x, y))
        return points_inside
    
    def generate_random_points(self, n):
        points = []
        for i in range(n):
            points.append((random.randint(self.x_range[0], self.x_range[1]), random.randint(self.y_range[0], self.y_range[1])))
        return points

# # Example usage
# n = 10  # Number of vertices in the polygon
# num_points_inside = 10000  # Number of points to generate inside the polygon
# dt = DataGeneration()

# # Generate the convex polygon
# convex_polygon = dt.generate_random_convex_polygon(n)

# # Generate points inside the convex polygon
# points_inside = dt.generate_points_inside_polygon(convex_polygon, num_points_inside)

# fig, ax = plt.subplots()
# x_inside, y_inside = zip(*points_inside)
# ax.scatter(x_inside, y_inside, color='black')
# x_hull, y_hull = zip(*convex_polygon)
# ax.scatter(x_hull, y_hull, color='red')
# ax.plot(*zip(*convex_polygon, convex_polygon[0]), color='red')
# ax.set_aspect('equal', 'box')
# plt.show()

# print("Convex Polygon Vertices:", convex_polygon)
# print("Points Inside Polygon:", points_inside)
