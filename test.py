#!/usr/bin/env python
import math
import random
from functools import partial
from math import cos, pi, sin

import numpy as np

import src.draw as draw
import src.vector as vector
from src.collidables import Collidables
from src.draw import h, height, w, width

bg = (100 / 255.0, 80 / 255.0, 80 / 255.0)
white = (1, 1, 1)
blue = (0, 0, 1)
red = (1, 0, 0)

draw.background(bg)

collidables = Collidables()

def draw_arc_with_segmented_lines(center, t1, t2, incr):
    for _ in range(0, 100):
        for r in range(0, width - incr, incr):
            for segment in range(0, math.floor(r / 10)):
                theta = t1 + (random.gauss(t2, pi))
                start = center[0] + r * sin(theta), center[1] + r * cos(theta)
                end = center[0] + (r + incr) * sin(theta), center[1] + (r + incr) * cos(
                    theta
                )
                draw.line((1, 1, 1), start, end, 0.2)


# draw_grid(10)


def draw_grid_of_circles(rows):
    for r in range(0, rows):
        cols = 10
        for c in range(0, cols):
            circle_origin = (
                (w / cols) * c + (w / (cols * 2)),
                (h / rows) * r + (h / (rows * 2)),
            )
            circle_radius = 5
            draw.circle(white, circle_origin, circle_radius, 2)
            collidables.add_circle(circle_origin, circle_radius)


# draw_grid_of_circles(10)

# for i in range(0, 5):
#     draw.starburst(
#         white,
#         collidables,
#         (int(random.uniform(0, width)), int(random.uniform(0, height))),
#         (random.uniform(10, 100)),
#         int(random.uniform(10, 100)),
#         draw_only_collisions=True,
#     )

# Draw a line
# starting from random points on that line, draw some new lines

def is_np(a):
    return 'numpy' in str(type(a))

class Line:
    def __init__(self, start, end):
        assert(is_np(start))
        assert(is_np(end))
        assert(len(start) == 2)
        assert(len(end) == 2)
        self.start = start
        self.end = end
        self.direction = self.end - self.start
        self.direction_norm = vector.norm(self.direction)

    def p(self, t):
        """0.0 <= t < 1.0"""
        return self.direction * t + self.start

    def draw(self):
        draw.line(white, self.start, self.end, 1)
    
    def __str__(self) -> str:
        return (f"{self.start}, {self.end}")

    @staticmethod
    def create_random():
        return Line(
            np.array((random.uniform(0.25 * w, 0.75 * w), random.uniform(0.25 * h, 0.75 * h))),
            np.array((random.uniform(0.25 * w, 0.75 * w), random.uniform(0.25 * h, 0.75 * h))),
        )

    @staticmethod
    def create_ray(start, direction, max_length=w, collisions=True):
        if collisions:
            collisions = collidables.ray_intersections(start, direction, max_length)
            if len(collisions) > 0:
                end = collisions[0]
            else:
                end = start + direction * max_length
        else:
            end = start + direction * max_length
        return Line(np.array(start), np.array(end))


# line = Line((100, 100), (200, 200))
line = Line.create_random()
line.draw()
q = [(6, line)]
while len(q) > 0:
    rem, line = q.pop()
    for i in range(0, 10):
        p = line.p(random.uniform(0.0, 1.0))
        deg = 60
        # rot = random.choice([-90, 90])
        rot = random.choice([-deg, deg])
        direction = vector.rotate_deg(rot, line.direction_norm)
        l = Line.create_ray(p, direction, max_length=200, collisions=True)
        collidables.add_line(l)
        l.draw()
        if rem > 0 and random.uniform(0, 1) > 0.8:
            q.append((rem - 1, l))


# for i in range(0, 10):
# start = (int(random.uniform(0, width)), int(random.uniform(0, height)))
# direction = vector.norm(np.array([random.uniform(0, 1), random.uniform(-1, 1)]))
# max_length = 300
# start = (0, 0)
# direction = (1, 1)
# draw_ray_with_collisions(start, direction, max_length)


# for i in range(0, 10):
#     circle_origin = (w / 10 * i + w / 2, h / 2)
#     circle_radius = 500
#     ray_origin = (200, h / 2)
#     ray_direction = (-1, -0.5 + 0.08 * i)

#     draw_circle(c, white, circle_origin, circle_radius, 2)

#     collidables.add_circle(circle_origin, circle_radius)

# for i in range(0, 10):
#     intersections = vector.intersect_ray_with_circle(
#         ray_origin, ray_direction, circle_origin, circle_radius
#     )
#     print(intersections)
#     if len(intersections) > 0:
#         draw_line(c, white, ray_origin, intersections[0], 2)

# if len(intersections) == 2:
#     draw_circle(c, red, intersections[0], 1, 10)
#     draw_circle(c, blue, intersections[1], 1, 10)
#     draw_line(c, white, ray_origin, intersections[0], 2)
# elif len(intersections) == 1:
#     draw_circle(c, red, intersections[0], 1, 10)
#     draw_line(c, white, ray_origin, intersections[0], 2)

# for i in range(0, 10):
#     starburst(
#         (int(random.uniform(0, width)), int(random.uniform(0, height))),
#         (random.uniform(10, 300)),
#         int(random.uniform(10, 100)),
#         draw_only_collisions=True,
#     )

if __name__ == "__main__":
    draw.s.write_to_png("example.png")  # Output to PNG
    draw.s.finish()
