import math

import numpy as np


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


def intersect_circle(ray_origin, ray_direction, circle_origin, circle_radius):
    """

    >>> line_start = (0,0)
    >>> line_dir   = (1,0)
    >>> circle_origin = (0,0)
    >>> circle_radius = 10
    >>> print(intersect_circle(line_start, line_dir, circle_origin, circle_radius))
    (array([10.,  0.]), array([-10.,   0.]))
    >>>
    >>> # horizontal and vertical line centered at circle
    >>> circle_origin = (0,0)
    >>> circle_radius = 3
    >>> line_start = (0,0)
    >>> line_dir   = (1,0)
    >>> print(intersect_circle(line_start, line_dir, circle_origin, circle_radius))
    (array([3., 0.]), array([-3.,  0.]))
    >>> line_start = (0,0)
    >>> line_dir   = (0,1)
    >>> print(intersect_circle(line_start, line_dir, circle_origin, circle_radius))
    (array([0., 3.]), array([ 0., -3.]))
    >>>
    >>> # line outside the circle
    >>> circle_origin = (0,0)
    >>> circle_radius = 3
    >>> line_start = (4,0)
    >>> line_dir   = (0,1)
    >>> print(intersect_circle(line_start, line_dir, circle_origin, circle_radius))
    (array([3., 0.]), array([-3.,  0.]))
    """
    center = np.array(circle_origin, dtype=float)
    p0 = np.array(ray_origin)
    direc = np.array(ray_direction)
    p1 = p0 + direc
    oc = p0 - center
    a = dist_sq(p0, p1)
    b = np.dot(p1, oc)
    c = dist_sq(p0, center) - circle_radius ** 2
    disc = b ** 2 - (a * c)
    if disc < 0:
        # no roots exist
        return None

    disc_root = math.sqrt(disc)
    t0 = (-b + disc_root) / a
    t1 = (-b - disc_root) / a
    print(t0, t1)

    def point(t):
        return direc * t + p0

    return (point(t0), point(t1))


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
    t1 = np.cross(v2, v1) / np.dot(v2, v3)
    t2 = np.dot(v1, v3) / np.dot(v2, v3)
    if t1 >= 0.0 and t2 >= 0.0 and t2 <= 1.0:
        return [rayOrigin + t1 * rayDirection]
    return []


if __name__ == "__main__":
    import doctest

    doctest.testmod()
