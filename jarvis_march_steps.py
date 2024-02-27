import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
import time

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
    convex_hull_steps = []
    convex_hull_process = []
    p = first
    while True:
        convex_hull.append(points[p])
        convex_hull_steps.append(convex_hull.copy())
        q = (p + 1) % n
        for r in range(n):
            if determinant_orientation(points[p], points[q], points[r]) == 2:
                q = r
                convex_hull_process = convex_hull.copy() + [points[q]]
                convex_hull_steps.append(convex_hull_process)
        p = q
        if p == first:
            break
    convex_hull.append(convex_hull[0]) # added the starting point again to close the convex hull
    #convex_hull_steps.append(convex_hull.copy())
    return convex_hull_steps

def random_points(n):
    return [(random.randint(0, 1000), random.randint(0, 1000)) for i in range(n)]

# def plot_points(points, hull):
#     x = [p[0] for p in points]
#     y = [p[1] for p in points]
#     hull_x = [p[0] for p in hull]
#     hull_y = [p[1] for p in hull]
#
#     plt.title("Jarvis March")
#     plt.xlabel("x-axis")
#     plt.ylabel("y-axis")
#     plt.scatter(x, y, 10, color = "black")
#     plt.plot(hull_x, hull_y, color = "red")
#     plt.show()



# Plot the steps of the algorithm
def plot_convex_hull_steps():
    for i, convex_hull in enumerate(convex_hull_steps[1::]):
        plt.subplot(6, 4, i + 1)
        plt.plot([x for x, y in points], [y for x, y in points], 'bo')  # Plot the points
        plt.plot([x for x, y in convex_hull], [y for x, y in convex_hull], 'r-')  # Plot the convex hull
        plt.title(f"Step {i + 1}")

points = random_points(10)
# jm = jarvis_march(points)
# print(jm)
# plot_points(points, jm)
convex_hull_steps = jarvis_march(points)

# Print the final convex hull
if convex_hull_steps:
    print(convex_hull_steps[-1])  # The last step contains the final convex hull
else:
    print("No convex hull found.")

plot_convex_hull_steps()
plt.show()
# def main():
#     # points = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
#     points = random_points(100)
#     jm = jarvis_march(points)
#     print(jm)
#     plot_points(points, jm)
#
# if __name__ == "__main__":
#     main()
