import timeit
from graham_display import graham_scan
from jarvis_march import jarvis_march
import matplotlib.pyplot as plt
import random

def random_points(n):
    return [(random.randint(0, 32767), random.randint(0, 32767)) for i in range(n)]

def chans_algorithm(points = [], plot = True):

    pts = points
    if len(pts) == 0:
        pts = random_points(100)

    t = 0
    m = min(2 ** (2 ** t), len(pts))
    hull = []

    while True:
        if hull and len(hull) <= m:
            break
        subsets = []
        for i in range(0, len(pts), m):
            subsets.append(pts[i:i + m])
        # print(f"Subsets: {subsets}")

        hulls = []
        for subset in subsets:
            hulls.append(graham_scan(points=subset, plot=False))

        flat_hulls = []
        for hull in hulls:
            for point in hull:
                flat_hulls.append(point)
        hull = jarvis_march(flat_hulls)

        t += 1
        m = min(2 ** (2 ** t), len(pts))

    if plot:
        x = [p[0] for p in flat_hulls]
        y = [p[1] for p in flat_hulls]
        hull_x = [p[0] for p in hull]
        hull_y = [p[1] for p in hull]
        plt.title("Chan's Algorithm")
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.scatter(x, y, 10, color = "black")
        plt.plot(hull_x, hull_y, color = "red")
        plt.show()
    return hull

# chans_algorithm()
# print(timeit.timeit(lambda: chans_algorithm(plot=False), number=1))
