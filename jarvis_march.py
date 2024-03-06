import matplotlib.pyplot as plt
import random
import timeit

def jarvis_march(pts=[], plot=True):
    # Initialize the list of points
    points = pts

    # Function to find the index of the leftmost point
    def left_most_index(points):
        first_index = 0
        for i in range(1, len(points)):
            if points[i][0] < points[first_index][0]:
                first_index = i
            elif points[i][0] == points[first_index][0]:
                if points[i][1] > points[first_index][1]:
                    first_index = i
        return first_index

    # Function to determine the orientation of three points
    def determinant_orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - p[0]) - (q[0] - p[0]) * (r[1] - p[1])

        if val == 0:
            return 0  # Collinear
        elif val > 0:
            return 1  # Clockwise
        else:
            return 2  # Counterclockwise

    # Function to plot the points and the convex hull if required
    def plot_points(points, hull):
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        hull_x = [p[0] for p in hull]
        hull_y = [p[1] for p in hull]

        plt.title("Jarvis March")
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.scatter(x, y, 10, color="black")
        plt.plot(hull_x, hull_y, color="red")
        plt.show()

    # Ensure there are at least 3 points to form a polygon
    n = len(points)
    if n < 3:
        return

    # Start the Jarvis March algorithm
    first = left_most_index(points)
    convex_hull = []
    p = first
    while True:
        convex_hull.append(points[p])
        q = (p + 1) % n
        for r in range(n):
            if determinant_orientation(points[p], points[q], points[r]) == 2:
                q = r
        p = q
        if p == first:
            break

    # Close the convex hull by adding the starting point again
    convex_hull.append(convex_hull[0])

    # Plot the points and the convex hull if plot is True
    if plot:
        plot_points(points, convex_hull)

    return convex_hull


# jarvis_march()
# print(timeit.timeit(stmt = "jarvis_march(plot = False)", setup="from __main__ import jarvis_march", number=1))

