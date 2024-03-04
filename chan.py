import math
import timeit
from graham_display import graham_scan
import matplotlib.pyplot as plt
import random
import data_generation_convex_polygon as dgp

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
        pts = random_points(100)
    n = len(pts)
    m = int(math.sqrt(n))
    t = 1
    while True:
        m = min(m, n)
        subsets = [pts[i:i + m] for i in range(0, n, m)]
        hulls = [graham_scan(subset, plot=False) for subset in subsets]
        p0 = min(min(hulls), key=lambda p: p[0])
        final_hull = []
        pthis = p0
        if plot:
            fig, ax = plt.subplots()
        colors = [(random.random()/10, random.random()/10, random.random()) for _ in range(len(hulls))]

        for _ in range(1, m+1):
        # for k in range(1, m+1):
            if plot:
                ax.clear()
                ax.set_title("Chan's Algorithm")
                ax.set_xlabel("x-axis")
                ax.set_ylabel("y-axis")
                ax.scatter(*zip(*pts), 10, color='black')
                for i, hull in enumerate(hulls):
                    color = colors[i]
                    for j in range(len(hull)):
                        ax.scatter(*hull[j], 10, color=color)
                        ax.plot(*zip(*[hull[j-1], hull[j]]), color=color)
                    ax.plot(*zip(*[hull[-1], hull[0]]), color=color)
            tangents = []
            for hull in hulls:
                tangent = search_tangent(hull, pthis)
                tangents.append(tangent)
            if plot:
                ax.scatter(*zip(*tangents), 10, color='red')
            most_cw_tangent = tangents[0]
            for i in range(1, len(tangents)):
                if orientation(pthis, most_cw_tangent, tangents[i]) < 0:
                    most_cw_tangent = tangents[i]
            pthis = most_cw_tangent
            final_hull.append(most_cw_tangent)
            if plot:
                ax.plot(*zip(*final_hull, final_hull[0]), color='green')
                ax.scatter(*most_cw_tangent, 10, color='yellow')
                for point in final_hull:
                    plt.scatter(*point, 10, color='green')
                plt.pause(0.01)
            if pthis == p0:
                if plot:
                    plt.tight_layout()
                    plt.show()
                return final_hull
        t += 1
        m = min(2**(2**t), len(pts))
        print(m)
    return "incomplete"

hull = dgp.DataGeneration(100, 100).generate_random_convex_polygon(32)
points = hull + dgp.DataGeneration(100, 100).generate_points_inside_polygon(hull, 68)
print(chans_algorithm(points))
# print(timeit.timeit(lambda: chans_algorithm(plot=False), number=1))