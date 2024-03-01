import math
import timeit

import numpy as np
from graham_display import graham_scan
from jarvis_march import jarvis_march
import matplotlib.pyplot as plt
import random

def chans_algorithm(points = [], plot = True):

    def random_points(n):
        for i in range(n):
            points.append((random.randint(0, 32767), random.randint(0, 32767)))
        return points

    pts = points
    if len(pts) == 0:
        pts = random_points(1000000)

    m = max(1, int(math.sqrt(len(pts))))
    hull = []
            
    def orientation(p, q, r):
        val = (q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1])
        return (val > 0) - (val < 0)

    def search_tangent(subset, p):
        left, right = 0, len(subset)
        lprev = orientation(p, subset[0], subset[-1])
        lnext = orientation(p, subset[0], subset[(left + 1) % right])
        while left < right:
            mid = (left + right) // 2
            mprev = orientation(p, subset[mid], subset[(mid - 1) % len(subset)])
            mnext = orientation(p, subset[mid], subset[(mid + 1) % len(subset)])
            mside = orientation(p, subset[left], subset[mid])
            if mprev != -1 and mnext != -1:
                return subset[mid]
            elif mside == 1 and (lnext == -1 or lprev == lnext) or mside == -1 and mprev == -1:
                right = mid
            else:
                left = mid + 1
                lprev = -mnext
                lnext = orientation(p, subset[left], subset[(left + 1) % len(subset)]) - 1
        return subset[0]

    while True:
        subsets = [pts[i:i + m] for i in range(0, len(pts), m)]
        hulls = [graham_scan(points=subset, plot=False) for subset in subsets]
        point_on_hull = min(min(hulls), key=lambda p: p[0])
        hull = [point_on_hull]
        for _ in range(len(pts)):
            next_points = [search_tangent(subset, point_on_hull) for subset in hulls]
            next_point = max(next_points, key=lambda p: (p[0] - point_on_hull[0], p[1] - point_on_hull[1]))
            if next_point == hull[0]:
                break
            hull.append(next_point)
            point_on_hull = next_point
        if len(hull) <= m:
            break
        m *= 2

    if plot:
        x = [p[0] for p in pts]
        y = [p[1] for p in pts]
        hull_x = [p[0] for p in hull]
        hull_y = [p[1] for p in hull]
        plt.title("Chan's Algorithm")
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.scatter(x, y, 10, color = "black")
        plt.plot(hull_x, hull_y, color = "red")
        plt.show()
    return hull

# def generate_random_points(num_points):
#     return [(random.randint(0, 32767), random.randint(0, 32767)) for _ in range(num_points)]

# def plot_points(points, hull, tangent_point, start_point):
#     plt.figure()
#     xs, ys = zip(*points)
#     plt.scatter(xs, ys, 10, color='black')
#     plt.scatter([start_point[0]], [start_point[1]], 10, color='blue')
#     hull_xs, hull_ys = zip(*hull)
#     plt.scatter(hull_xs, hull_ys, 10, color='green')
#     plt.scatter([tangent_point[0]], [tangent_point[1]], 10, color='red')
#     plt.plot([start_point[0], tangent_point[0]], [start_point[1], tangent_point[1]], 'red')
#     hull_lines = hull + [hull[0]]
#     xs, ys = zip(*hull_lines)
#     plt.plot(xs, ys, 'green')
#     plt.show()

# points = generate_random_points(100)
# hull = graham_scan(points, plot=False)
# start_point = (32767,0)
# tangent_point = search_tangent(hull, start_point)
# plot_points(points, hull, tangent_point, start_point)

#chans_algorithm()