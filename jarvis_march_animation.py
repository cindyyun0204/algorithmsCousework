import matplotlib.pyplot as plt
import random
import timeit

def jarvis_march(pts = [], plot = True):

    points = pts

    def random_points(n):
        for i in range(n):
            points.append((random.randint(0, 32767), random.randint(0, 32767)))
        return points
    
    if len(points) == 0:
        points = random_points(100)

    def left_most_index(points):
        first_index = 0
        for i in range(1, len(points)):
            if points[i][0] < points[first_index][0]:
                first_index = i
            elif points[i][0] == points[first_index][0]:
                if points[i][1] > points[first_index][1]:
                    first_index = i
        return first_index

    def determinant_orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - p[0]) - (q[0] - p[0]) * (r[1] - p[1])

        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2
        
    def random_points(n):
        for i in range(n):
            points.append((random.randint(0, 32767), random.randint(0, 32767)))
        return points
    
    def plot_points(points, hull, next_point=None, compared_point=None):
        ax.clear()
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        hull_x = [p[0] for p in hull]
        hull_y = [p[1] for p in hull]
        ax.scatter(x, y, 10, color="black")  # All other points - black
        ax.plot(hull_x, hull_y, color="green")  # Hull points - green
        ax.scatter(hull[0][0], hull[0][1], 10, color="blue")  # Starting point - blue
        if next_point:
            ax.scatter(next_point[0], next_point[1], 10, color="red")  # The next point - red
            ax.plot([hull[-1][0], next_point[0]], [hull[-1][1], next_point[1]], color="red")
        if compared_point:
            ax.scatter(compared_point[0], compared_point[1], 10, color="yellow")  # The compared point - yellow
            ax.plot([hull[-1][0], compared_point[0]], [hull[-1][1], compared_point[1]], color="yellow")
        plt.pause(0.01)

    if plot:
        fig, ax = plt.subplots()

    n = len(points)
    if n < 3:
        return
    first = left_most_index(points)
    convex_hull = []
    p = first
    while True:
        convex_hull.append(points[p])
        q = (p + 1) % n
        for r in range(n):
            if determinant_orientation(points[p], points[q], points[r]) == 2:
                q = r
            if plot:
                plot_points(points, convex_hull, points[q], points[r])
        p = q
        if p == first:
            break
    convex_hull.append(convex_hull[0])
    return convex_hull

jarvis_march()
# print(timeit.timeit(stmt = "jarvis_march(plot = False)", setup="from __main__ import jarvis_march", number=1))

