import math
from math import cos, sin

import numpy as np

# np.seterr(all="raise")


def dist_sq(p0, p1):
    return (p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2


def dist(p0, p1):
    return math.sqrt(dist_sq(p0, p1))


def magnitude(vector):
    return np.sqrt(np.dot(np.array(vector), np.array(vector)))


def norm(vector):
    return np.array(vector) / magnitude(np.array(vector))


def direction(start, end):
    return norm(np.array(end) - np.array(start))


def rotate(radians, vector):
    rot = np.array([[cos(radians), -sin(radians)], [sin(radians), cos(radians)]])
    return np.around(np.dot(rot, vector), 5)


def rotate_deg(theta, vector):
    """
    >>> print(rotate_deg(90, (0, 1)))
    [-1.  0.]
    >>> print(rotate_deg(-45, (0, 1)))
    [0.70711 0.70711]
    """
    return rotate(np.deg2rad(theta), vector)


def intersect_line_with_circle_with_t(start, end, origin, radius):
    # https://math.stackexchange.com/questions/311921/get-location-of-vector-circle-intersection
    # https://bugfree.dk/blog/2018/09/03/ray-tracing-computing-ray-sphere-intersections
    """
    >>> origin = (0, 0)
    >>> radius = 1

    >>> # two
    >>> start  = (0, 0)
    >>> end    = (1, 0)
    >>> print(intersect_line_with_circle_with_t(start, end, origin, radius))
    [(-1.0, array([-1.,  0.])), (1.0, array([1., 0.]))]
    >>> start  = (0, 0)
    >>> end    = (1, 1)
    >>> print(intersect_line_with_circle_with_t(start, end, origin, radius))
    [(-0.7071067811865476, array([-0.70710678, -0.70710678])), (0.7071067811865476, array([0.70710678, 0.70710678]))]

    >>> # none
    >>> start  = (2, 0)
    >>> end    = (2, 1)
    >>> print(intersect_line_with_circle_with_t(start, end, origin, radius))
    []

    >>> # one
    >>> start  = (0, 1)
    >>> end    = (2, 1)
    >>> print(intersect_line_with_circle_with_t(start, end, origin, radius))
    [(0.0, array([0., 1.]))]
    """
    center = np.array(origin, dtype=float)
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    direc = end - start

    oc = start - center
    a = np.dot(direc, direc)
    b = np.dot(2 * direc, oc)
    c = np.dot(oc, oc) - radius ** 2
    disc = b ** 2 - 4 * (a * c)
    if disc < 0:
        return []

    disc_root = math.sqrt(disc)
    t0 = (-b + disc_root) / (2 * a)
    t1 = (-b - disc_root) / (2 * a)
    # print(a, b, disc_root, t0, t1)

    def point(t):
        return direc * t + start

    p0 = point(t0)
    if t0 == t1:
        return [(t0, p0)]

    p1 = point(t1)
    return [(t1, p1), (t0, p0)]


def intersect_line_with_circle(start, end, origin, radius):
    """
    >>> origin = (0, 0)
    >>> radius = 1

    >>> # two
    >>> start  = (0, 0)
    >>> end    = (1, 0)
    >>> print(intersect_line_with_circle(start, end, origin, radius))
    [array([-1.,  0.]), array([1., 0.])]
    >>> start  = (0, 0)
    >>> end    = (1, 1)
    >>> print(intersect_line_with_circle(start, end, origin, radius))
    [array([-0.70710678, -0.70710678]), array([0.70710678, 0.70710678])]

    >>> # none
    >>> start  = (2, 0)
    >>> end    = (2, 1)
    >>> print(intersect_line_with_circle(start, end, origin, radius))
    []

    >>> # one
    >>> start  = (0, 1)
    >>> end    = (2, 1)
    >>> print(intersect_line_with_circle(start, end, origin, radius))
    [array([0., 1.])]
    """
    return [
        p for (_, p) in intersect_line_with_circle_with_t(start, end, origin, radius)
    ]


def intersect_line_segment_with_circle(start, end, origin, radius):
    """
    >>> origin = (1, 0)
    >>> radius = 1

    >>> start  = (0, 0)
    >>> end    = (2, 0)
    >>> print(intersect_line_segment_with_circle(start, end, origin, radius))
    [array([0., 0.]), array([2., 0.])]

    >>> # one
    >>> start  = (1, 0)
    >>> end    = (1, 1)
    >>> print(intersect_line_segment_with_circle(start, end, origin, radius))
    [array([1., 1.])]
    """
    return [
        p
        for (t, p) in intersect_line_with_circle_with_t(start, end, origin, radius)
        if t >= 0.0 and t <= 1.0
    ]


def intersect_ray_with_circle(start, direction, origin, radius):
    """
    >>> origin = (2, 0)
    >>> radius = 1

    >>> # two
    >>> start  = (0, 0)
    >>> direction    = (1, 0)
    >>> print(intersect_ray_with_circle(start, direction, origin, radius))
    [array([1., 0.]), array([3., 0.])]

    >>> # none
    >>> start  = (0, 2)
    >>> direction    = (1, 0)
    >>> print(intersect_ray_with_circle(start, direction, origin, radius))
    []

    >>> # one
    >>> start  = (2, 0)
    >>> direction    = (1, 1)
    >>> print(intersect_ray_with_circle(start, direction, origin, radius))
    [array([2.70710678, 0.70710678])]
    """
    center = np.array(origin, dtype=float)
    start = np.array(start, dtype=float)
    direc = np.array(direction, dtype=float)
    end = start + direc
    return [
        point
        for (t, point) in intersect_line_with_circle_with_t(start, end, origin, radius)
        if t >= 0.0
    ]

def intersections_with_line_segments(origin, direction, segments):
    if len(segments) == 0:
        return []

    o = np.array(origin)
    d = np.array(direction)
    ps = np.array(segments)

    swapped = np.swapaxes(ps, 0, 1)
    p0 = swapped[0]
    p1 = swapped[1]

    v1 = o - p0 
    v2 = p1 - p0
    v3 = np.array([-d[1], d[0]])

    dot = np.dot(v2, v3)
    t1 = np.cross(v2, v1) / dot
    t2 = np.dot(v1, v3) / dot

    # Check the collision is within the line segment and ahead of the ray
    t1[(t1 < 0) | (t2 > 1) | (t2 < 0) | (np.isclose(t1, 0.0)) | (np.isclose(t2, 0.0))] = np.nan

    intersections = ((t1.reshape([-1, 1]) * d) + o)
    return intersections

def dist_to_many_points(origin, intersections):
    if len(intersections) == 0:
        return [], []

    v = np.square(intersections - origin)
    a, b = np.hsplit(v, [1])
    dists = a - b
    
    # sort
    d = np.append(intersections, dists, 1)
    d = d[~np.isnan(d).any(axis=1)] # remove NaNs
    d = d[d[:, 2].argsort()] # sort by distance
    intersections, d = np.hsplit(d, [2])
    
    return intersections, d

def intersect_ray_vector(rayOrigin, rayDirection, point1, point2):
    """
    >>> # Line segment
    >>> z1 = (0,0)
    >>> z2 = (10, 10)
    >>>
    >>> # Test ray 1 -- intersecting ray
    >>> r = (0, 5)
    >>> d = norm((1,0))
    >>> len(intersect_ray_vector(r,d,z1,z2)) == 1
    True
    >>> # Test ray 2 -- intersecting ray
    >>> r = (5, 0)
    >>> d = norm((0,1))
    >>> len(intersect_ray_vector(r,d,z1,z2)) == 1
    True
    >>> # Test ray 3 -- intersecting perpendicular ray
    >>> r0 = (0,10)
    >>> r1 = (10,0)
    >>> d = norm(np.array(r1)-np.array(r0))
    >>> len(intersect_ray_vector(r0,d,z1,z2)) == 1
    True
    >>> # Test ray 4 -- intersecting perpendicular ray
    >>> r0 = (0, 10)
    >>> r1 = (10, 0)
    >>> d = norm(np.array(r0)-np.array(r1))
    >>> len(intersect_ray_vector(r1,d,z1,z2)) == 1
    True
    >>> # Test ray 5 -- non intersecting anti-parallel ray
    >>> r = (-2, 0)
    >>> d = norm(np.array(z1)-np.array(z2))
    >>> len(intersect_ray_vector(r,d,z1,z2)) == 0
    True
    >>> # Test ray 6 --intersecting perpendicular ray
    >>> r = (-2, 0)
    >>> d = norm(np.array(z1)-np.array(z2))
    >>> len(intersect_ray_vector(r,d,z1,z2)) == 0
    True
    """
    # Convert to numpy arrays
    rayOrigin = np.array(rayOrigin, dtype=float)
    rayDirection = np.array(norm(rayDirection), dtype=float)
    point1 = np.array(point1, dtype=float)
    point2 = np.array(point2, dtype=float)

    # Ray-Line Segment Intersection Test in 2D
    # http://bit.ly/1CoxdrG
    v1 = rayOrigin - point1
    v2 = point2 - point1
    v3 = np.array([-rayDirection[1], rayDirection[0]])

    # print(point1, point2)
    # print(v1, v2, v3)
    t1 = np.cross(v2, v1) / np.dot(v2, v3)
    t2 = np.dot(v1, v3) / np.dot(v2, v3)

    if (
        t1 >= 0.0
        and t2 >= 0.0
        and t2 <= 1.0
        # We don't want to collide at our very start, eg if a ray is starting at an already existing line
        and not np.isclose(t1, 0.0)
        and not np.isclose(t2, 0.0)
    ):
        return [rayOrigin + t1 * rayDirection]
    return []


if __name__ == "__main__":
    import doctest

    doctest.testmod()
