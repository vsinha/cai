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

rows = 10
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


for i in range(0, 5):
    draw.starburst(
        white,
        collidables,
        (int(random.uniform(0, width)), int(random.uniform(0, height))),
        (random.uniform(10, 100)),
        int(random.uniform(10, 100)),
        draw_only_collisions=True,
    )

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
