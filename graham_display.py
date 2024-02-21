import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import timeit
from time import sleep

def graham_scan(points = None, randomize = True, plot = True):
    points = []

    def random_points(n):
        for i in range(n):
            points.append((random.randint(0, 100), random.randint(0, 100)))
        return points
    
    if randomize:
        random_points(100)
    else:
        points = points

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
    
    points = sort(points)
    p0 = points[0]

    fig, ax = plt.subplots()

    stack = []

    def cross_product(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    for i, p in enumerate(points):
        while len(stack) > 1 and cross_product(stack[-2], stack[-1], p) <= 0:
            stack.pop()
        stack.append(p)
        if plot:
            ax.clear()
            ax.scatter([x[0] for x in points], [x[1] for x in points], color="black")  # All other points - black
            ax.scatter(p0[0], p0[1], color="blue")  # Starting point - blue
            ax.scatter([x[0] for x in stack[1:]], [x[1] for x in stack[1:]], color="green")  # points in the stack - green
            if i < len(points) - 1:
                ax.scatter(points[i + 1][0], points[i + 1][1], color="red")  # The next point - red
            ax.plot([x[0] for x in stack] + [stack[0][0]], [x[1] for x in stack] + [stack[0][1]], color="green")
            plt.pause(0.01)
    stack.append(p0)
    
    if plot:
        plt.tight_layout()
        plt.show()
    return stack

graham_scan()