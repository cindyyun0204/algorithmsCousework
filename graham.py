import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import timeit
from time import sleep

def grahams_scan(points):
    sorted_points = sort(points)
    stack = []
    for p in sorted_points:
        while len(stack) > 1 and cross_product(stack[-2], stack[-1], p) <= 0:
            stack.pop()
        stack.append(p)
    stack.append(sorted_points[0]) # added the starting point again to close the convex hull
    return stack

def random_points(n):
        return [(random.randint(0, 1000), random.randint(0, 1000)) for i in range(n)]

def sort(points):
    def compare_angles(p1, p2):
        angle1 = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        angle2 = math.atan2(p2[1] - p0[1], p2[0] - p0[0])
        return angle1 < angle2
    
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if compare_angles(arr[j], pivot):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def quicksort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quicksort(arr, low, pi - 1)
            quicksort(arr, pi + 1, high)

    if len(points) < 3:
        return points
    p0 = min(points, key=lambda p: p[0])
    points.remove(p0)
    quicksort(points, 0, len(points) - 1)
    points.insert(0, p0)
    return points

def cross_product(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def plot_points(points, hull): # need to figure out where to put this function
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    hull_x = [p[0] for p in hull]
    hull_y = [p[1] for p in hull]

    plt.title("Graham's Scan")
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.scatter(x, y, 10, color = "black")
    plt.plot(hull_x, hull_y, color = "red")
    plt.show()

# points = [(0,0),(1,1),(3,2),(1,5),(0.5,5),(-1,3),(points-0.5,2),(3,3.5),(8,-1)]
    
points = random_points(500)
print(grahams_scan(points))
hull = grahams_scan(points)
plot_points(points, hull)