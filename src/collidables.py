import src.vector as vector
import numpy as np


class Collidables:
    def __init__(self):
        self.lines = []
        self.circles = []

    def add_line(self, start, end):
        self.lines.append((start, end))

    def add_line(self, line):
        self.lines.append([line.start, line.end])

    def add_circle(self, origin, radius):
        self.circles.append((origin, radius))

    def ray_intersections(self, start, direction, max_length=None):

        start = np.array(start)
        lines = np.array(self.lines)

        intersects = vector.intersections_with_line_segments(start, direction, lines)
        intersects, distances = vector.dist_to_many_points(start, intersects)

        # for (origin, radius) in self.circles:
        #     intersects += vector.intersect_ray_with_circle(
        #         start, direction, origin, radius
        #     )

        return intersects
