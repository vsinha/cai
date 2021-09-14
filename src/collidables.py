import src.vector as vector


class Collidables:
    lines = []
    circles = []

    def add_line(self, start, end):
        self.lines.append((start, end))

    def add_circle(self, origin, radius):
        self.circles.append((origin, radius))

    def ray_intersections(self, start, direction, max_length=None):
        intersects = []

        for (origin, radius) in self.circles:
            intersects += vector.intersect_ray_with_circle(
                start, direction, origin, radius
            )

        length_and_end = [(vector.dist(start, end), end) for end in intersects]
        if max_length is not None:
            length_and_end = [
                (length, end) for (length, end) in length_and_end if length < max_length
            ]

        length_and_end.sort(key=lambda x: x[0])
        return length_and_end