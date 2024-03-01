import math
import timeit
from graham_display import graham_scan
from jarvis_march import jarvis_march
import matplotlib.pyplot as plt
import random

def chans_algorithm(points = [], plot = True):

    def random_points(n):
        for i in range(n):
            points.append((random.randint(0, 32767), random.randint(0, 32767)))
        return points

    pts = points
    if len(pts) == 0:
        pts = random_points(10000)

    m = max(1, int(math.sqrt(len(pts))))
    hull = []
            
    while True:
        subsets = [pts[i:i + m] for i in range(0, len(pts), m)]
        hulls = [graham_scan(points=subset, plot=False) for subset in subsets]
        flat_hulls = [point for hull in hulls for point in hull]
        hull = jarvis_march(pts=flat_hulls, plot=False)
        if len(hull) <= m:
            break
        m *= 2

        # with search_tangent and a jarivs-march-like approach based on paper's pesudocode, not efficient
        # while True:
        #     subsets = [pts[i:i + m] for i in range(0, len(pts), m)]
        #     hulls = [graham_scan(points=subset, plot=False) for subset in subsets]
        #     point_on_hull = min(min(hulls), key=lambda p: p[0])
        #     hull = [point_on_hull]
        #     for k in range(len(pts)):
        #         next_points = []
        #         for subset in hulls:
        #             next_points.append(search_tangent(subset, point_on_hull))
        #         next_point = max(next_points, key=lambda p: (p[0] - point_on_hull[0], p[1] - point_on_hull[1]))
        #         hull.append(next_point)
        #         point_on_hull = next_point
        #     if len(hull) <= m:
        #         break
        #     m *= 2

    if plot:
        x = [p[0] for p in pts]
        y = [p[1] for p in pts]
        hull_x = [p[0] for p in hull]
        hull_y = [p[1] for p in hull]
        plt.title("Chan's Algorithm")
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.scatter(x, y, 10, color = "black")
        plt.plot(hull_x, hull_y, color = "red")
        plt.show()
    return hull
 
# def random_points(n):
#     points = []
#     for i in range(n):
#         points.append((random.randint(0, 32767), random.randint(0, 32767)))
#     return points

# logarithmic
def crossProduct(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def isSatisfied(p1,p2,externalPoint,hull):
    initialOrientation = crossProduct(externalPoint,p1,p2)
    for point in hull:
        if point == p1 or point == p2:
            continue
        orientation = crossProduct(externalPoint,p1,point)
        if initialOrientation == 0:
            continue
        if (initialOrientation > 0 and orientation < 0) or (initialOrientation < 0 and orientation > 0):
            return False
    return True

def moveLeft(midPoint, prevPoint, nextPoint, externalPoint):
    prevOrientation = crossProduct(externalPoint, midPoint, prevPoint)
    nextOrientation = crossProduct(externalPoint,midPoint,nextPoint)

    if nextOrientation < 0 and prevOrientation > 0:
        return True
    if nextOrientation > 0 and prevOrientation > 0:
        return True
    
    return False

def search_tangent(convexHull, externalPoint):
    left = 0
    right = len(convexHull) - 1
    

    while left <= right:
        mid = (left + right) // 2
        midNext = (mid + 1) % len(convexHull)
        midPrev = (mid - 1 + len(convexHull)) % len(convexHull)

        midPoint = convexHull[mid]
        nextPoint = convexHull[midNext]
        prevPoint = convexHull[midPrev]

        if isSatisfied(midPoint,nextPoint,externalPoint,convexHull):
            return midPoint
        elif moveLeft(midPoint,prevPoint,nextPoint,externalPoint):
            right = mid - 1
        else:
            left = mid + 1



# Example usage
# p0 = (0, 0)  # Example external point
# subset = [(1, 2), (2, 4), (4, 3), (3, 1)]  # Example convex hull points, sorted clockwise or counterclockwise
# tangent_point = search_tangent(subset, p0)
# print("Tangent point:", tangent_point)


#linear
# def crossProduct(p1, p2, p3):
#     return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
    
# def isTangent(externalPoint, point, hull):
#     isLeft = None
#     for hullPoint in hull:
#         if hullPoint == point:
#             continue
#         orientation = crossProduct(externalPoint, point, hullPoint)
#         if orientation == 0:
#             continue
#         if isLeft == None:
#             isLeft = orientation > 0
#         elif orientation > 0 != isLeft:
#             return False
#     if isLeft != None:
#         return True
#     else:
#         return False

# def search_tangent(convexHull, externalPoint):
#     for point in convexHull:
#         if isTangent(externalPoint, point, convexHull):
#             return point

#chans_algorithm()

subset = graham_scan([(random.randint(0, 32767), random.randint(0, 32767)) for _ in range(10)], plot=False)
p0 = (0,0) #SHould test all four coners
tangent_point = search_tangent(subset, p0)
xs, ys = zip(*subset)
plt.scatter(xs, ys, 10, color='black')
plt.scatter(p0[0], p0[1], 10, color='blue')
plt.scatter(tangent_point[0], tangent_point[1], 10, color='red')
plt.plot([p0[0], tangent_point[0]], [p0[1], tangent_point[1]], color='red')
plt.show()

#print(timeit.timeit(lambda: chans_algorithm(plot=False), number=1))