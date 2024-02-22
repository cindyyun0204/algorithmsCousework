import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import timeit
from time import sleep

def graham_scan(points = [], plot = True):
    pts = []

    def random_points(n):
        for i in range(n):
            pts.append((random.randint(0, 32767), random.randint(0, 32767)))
        return pts
    
    pts = points
    if len(pts) == 0:
        pts = random_points(1000000)

    # def sort(pts):
    #     def compare_angles(p1, p2):
    #         angle1 = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    #         angle2 = math.atan2(p2[1] - p0[1], p2[0] - p0[0])
    #         return angle1 < angle2
    #     def partition(arr, low, high):
    #         pivot = arr[high]
    #         i = low - 1
    #         for j in range(low, high):
    #             if compare_angles(arr[j], pivot):
    #                 i += 1
    #                 arr[i], arr[j] = arr[j], arr[i]
    #         arr[i + 1], arr[high] = arr[high], arr[i + 1]
    #         return i + 1
    #     def quicksort(arr, low, high):
    #         if low < high:
    #             pi = partition(arr, low, high)
    #             quicksort(arr, low, pi - 1)
    #             quicksort(arr, pi + 1, high)
    #     if len(pts) < 3:
    #         return pts
    #     p0 = min(pts, key=lambda p: p[0])
    #     pts.remove(p0)
    #     quicksort(pts, 0, len(pts) - 1)
    #     pts.insert(0, p0)
    #     return pts
        
    def sort(pts):
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
        if len(pts) < 3:
            return pts
        p0 = min(pts, key=lambda p: p[0])
        pts.remove(p0)
        pts.sort(key=lambda p: math.atan2(p[1] - p0[1], p[0] - p0[0]))
        pts.insert(0, p0)
        return pts
    
    pts = sort(pts)
    p0 = pts[0]
    if plot:
        fig, ax = plt.subplots()

    stack = []

    def cross_product(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    for i, p in enumerate(pts):
        while len(stack) > 1 and cross_product(stack[-2], stack[-1], p) <= 0:
            stack.pop()
        stack.append(p)
        if plot:
            ax.clear()
            ax.scatter([x[0] for x in pts], [x[1] for x in pts], 10, color="black")  # All other points - black
            ax.scatter(p0[0], p0[1], 10, color="blue")  # Starting point - blue
            ax.scatter([x[0] for x in stack[1:]], [x[1] for x in stack[1:]], 10, color="green")  # points in the stack - green
            if i < len(pts) - 1:
                ax.scatter(pts[i + 1][0], pts[i + 1][1], 10, color="red")  # The next point - red
            ax.plot([x[0] for x in stack] + [stack[0][0]], [x[1] for x in stack] + [stack[0][1]], 10, color="green")
            plt.pause(0.01)
    stack.append(p0)
    
    if plot:
        plt.tight_layout()
        plt.show()
    stack.pop()
    return stack

# graham_scan()
# print(timeit.timeit(stmt = "graham_scan(plot=False)", setup = "from __main__ import graham_scan", number = 1))