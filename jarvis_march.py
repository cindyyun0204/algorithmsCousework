import matplotlib.pyplot as plt
import random

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

def jarvis_march(points):
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
        p = q
        if p == first:
            break
    convex_hull.append(convex_hull[0]) # added the starting point again to close the convex hull
    return convex_hull

def random_points(n):
    return [(random.randint(0, 1000), random.randint(0, 1000)) for i in range(n)]

def plot_points(points, hull):
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    hull_x = [p[0] for p in hull]
    hull_y = [p[1] for p in hull]

    plt.title("Jarvis March")
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.scatter(x, y, 10, color = "black")
    plt.plot(hull_x, hull_y, color = "red")
    plt.show()

def main():
    # points = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
    points = random_points(100)
    print(jarvis_march(points))
    plot_points(points, jarvis_march(points))
    
if __name__ == "__main__":
    main()
