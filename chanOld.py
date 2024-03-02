import math
import timeit
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

    m = int(math.sqrt(len(pts)))
    hull = []
    t = 1

    while True:
        t += 1
        subsets = [pts[i:i + m] for i in range(0, len(pts), m)]
        hulls = [graham_scan(points=subset, plot=False) for subset in subsets]
        flat_hulls = [point for hull in hulls for point in hull]
        hull = jarvis_march(pts=flat_hulls, plot=False)
        if len(hull) <= m:
            break
        m = min(2**(2**t), len(pts))

        # with search_tangent and a jarivs-march-like approach based on paper's pesudocode, not efficient
        # while True:
        #     subsets = [pts[i:i + m] for i in range(0, len(pts), m)]
        #     hulls = [graham_scan(points=subset, plot=False) for subset in subsets]
        #     point_on_hull = min(min(hulls), key=lambda p: p[0])
        #     hull = [point_on_hull]
        #     for k in range(len(pts)):
        #         next_points = []
        #         for subset in hulls:
        #             next_points.append(search_tangent(subset, point_on_hull))
        #         next_point = max(next_points, key=lambda p: (p[0] - point_on_hull[0], p[1] - point_on_hull[1]))
        #         hull.append(next_point)
        #         point_on_hull = next_point
        #     if len(hull) <= m:
        #         break
        #     m *= 2

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

# def random_points(n):
#     points = []
#     for i in range(n):
#         points.append((random.randint(0, 32767), random.randint(0, 32767)))
#     return points

# Attempted to be logarithmic (not working in some cases)
# def search_tangent(subset, p0):
#     def cross_product(o, a, b):
#         return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
#     left = 0
#     right = len(subset)-1
#     while left < right:
#         mid = (left + right) // 2
#         if cross_product(p0, subset[mid], subset[(mid + 1) % len(subset)]) >= 0 and cross_product(p0, subset[mid], subset[(mid - 1) % len(subset)]) >= 0:
#             return subset[mid]
#         if cross_product(p0, subset[0], subset[mid]) >= 0:
#             right = mid
#         else:
#             if cross_product(p0, subset[mid], subset[(mid + 1) % len(subset)]) >= 0:
#                 right = mid
#             else:
#                 left = mid
#     return subset[0]

# linear
# def search_tangent(subset, p0):
#     def slope(p1, p2):
#         return (p2[1] - p1[1]) / (p2[0] - p1[0]) if p2[0] != p1[0] else float('inf')
#     min_slope = float('inf')
#     min_point = None
#     for point in subset:
#         current_slope = slope(p0, point)
#         if current_slope < min_slope:
#             min_slope = current_slope
#             min_point = point
#     return min_point

# chans_algorithm()
print(timeit.timeit(lambda: chans_algorithm(plot=False), number=1))