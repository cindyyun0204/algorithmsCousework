import random
import math
# import matplotlib.pyplot as plt

def random_points(n):
    return [(random.random(), random.random()) for i in range(n)]

def cross_product(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def sort_points(points):
    points.sort(key=lambda p: (p[0], p[1])) # impossible to have two points with the same x-coordinates if randomly generated tho
    p0 = points[0]
    # print(p0)
    points = points[1:]
    points.sort(key=lambda p: (math.atan2(p[1] - p0[1], p[0] - p0[0], p[0], p[1])))
    return [p0] + points

def graham_scan(points):
    sorted_points = sort_points(points)
    stack = []
    for p in sorted_points:
        while len(stack) > 1 and cross_product(stack[-2], stack[-1], p) <= 0:
            stack.pop()
        stack.append(p)
    return stack

print(graham_scan([(0,0),(1,1),(3,2),(1,5),(0.5,5),(-1,3),(-0.5,2),(3,3.5)]))