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

def javis_march(points,n):
    n = len(points)
    if n < 3:
        return
    first = left_most_index(points)
    convex_hull = []
    p = first
    while True:
        convex_hull.append(p)
        q = (p + 1) % n
        for r in range(n):
            if determinant_orientation(points[p], points[q], points[r]) == 2:
                q = r
        p = q
        if p == first:
            break
    return convex_hull

points = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
new = javis_march(points, len(points))
print(new)
