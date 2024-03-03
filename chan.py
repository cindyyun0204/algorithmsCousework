import math
import timeit
from graham_display import graham_scan
import matplotlib.pyplot as plt
import random

def chans_algorithm(points = [], plot = True):
    def random_points(n):
        for i in range(n):
            points.append((random.randint(0, 32767), random.randint(0, 32767)))
        return points

    def orientation(p, q, r):
        val = (q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1])
        return (val > 0) - (val < 0)

    def search_tangent(subset, p):
        if p in subset:
            return subset[(subset.index(p) + 1) % len(subset)]
        left, right = 0, len(subset)
        lprev = orientation(p, subset[0], subset[-1])
        lnext = orientation(p, subset[0], subset[(left + 1) % right])
        while left < right:
            mid = (left + right) // 2
            mprev = orientation(p, subset[mid], subset[(mid - 1) % len(subset)])
            mnext = orientation(p, subset[mid], subset[(mid + 1) % len(subset)])
            mside = orientation(p, subset[left], subset[mid])
            if mprev != -1 and mnext != -1:
                return subset[mid]
            elif mside == 1 and (lnext == -1 or lprev == lnext) or mside == -1 and mprev == -1:
                right = mid
            else:
                left = mid + 1
                lprev = -mnext
                lnext = orientation(p, subset[left-1], subset[(left + 1) % len(subset)])
        return subset[0]
    
    pts = points
    if len(pts) == 0:
        pts = random_points(1000)

    m = int(math.sqrt(len(pts)))
    subsets = [pts[i:i + m] for i in range(0, len(pts), m)]
    hulls = [graham_scan(subset, plot=False) for subset in subsets]
    p0 = min(pts, key=lambda p: p[0])
    final_hull = []
    pthis = p0
    if plot:
        fig, ax = plt.subplots()

    while True:
        if plot:
            ax.clear()
            for hull in hulls:
                color = (random.random()/10, random.random()/10, random.random())
                for i in range(len(hull)):
                    ax.scatter(*hull[i], 10, color=color)
                    ax.plot(*zip(*[hull[i-1], hull[i]]), color=color)
                ax.plot(*zip(*[hull[-1], hull[0]]), color=color)
        tangents = []
        for hull in hulls:
            tangent = search_tangent(hull, pthis)
            tangents.append(tangent)
        ax.scatter(*zip(*tangents), 10, color='red')
        most_cw_tangent = tangents[0]
        for i in range(1, len(tangents)):
            if orientation(pthis, most_cw_tangent, tangents[i]) < 0:
                most_cw_tangent = tangents[i]
        pthis = most_cw_tangent
        final_hull.append(most_cw_tangent)
        ax.scatter(*most_cw_tangent, 10, color='yellow')
        ax.plot(*zip(*final_hull, final_hull[0]), color='green')
        for point in final_hull:
            plt.scatter(*point, 10, color='green')
        plt.pause(0.01)
        if pthis == p0:
            break
    plt.show()
    return final_hull
        

# def plot_results(P, hull):
#     plt.scatter(*zip(*P), color='black')
#     if hull:
#         hull.append(hull[0])
#         plt.plot(*zip(*hull), color='red')
#     plt.show()

# def random_points(n):  
#     return [(random.randint(0, 32767), random.randint(0, 32767)) for i in range(n)]
# P = random_points(1000)
# m = 3
# hull = chans_algorithm(P, m)
# plot_results(P, hull)
    

# def generate_random_points(num_points):
#     return [(random.randint(0, 32767), random.randint(0, 32767)) for _ in range(num_points)]

# def plot_points(points, hull, tangent_point, start_point):
#     plt.figure()
#     xs, ys = zip(*points)
#     plt.scatter(xs, ys, 10, color='black')
#     plt.scatter([start_point[0]], [start_point[1]], 10, color='blue')
#     hull_xs, hull_ys = zip(*hull)
#     plt.scatter(hull_xs, hull_ys, 10, color='green')
#     plt.scatter([tangent_point[0]], [tangent_point[1]], 10, color='red')
#     plt.plot([start_point[0], tangent_point[0]], [start_point[1], tangent_point[1]], 'red')
#     hull_lines = hull + [hull[0]]
#     xs, ys = zip(*hull_lines)
#     plt.plot(xs, ys, 'green')
#     plt.show()

# points = generate_random_points(100)
# hull = graham_scan(points, plot=False)
# start_point = (32767,0)
# tangent_point = search_tangent(hull, start_point)
# plot_points(points, hull, tangent_point, start_point)
chans_algorithm()