#!/usr/bin/env python
import math
import random
from functools import partial
from math import cos, pi, sin

import cairo
import numpy as np

import src.vector as vector

width = w = 500
height = h = 500
bg = (100 / 255.0, 80 / 255.0, 80 / 255.0)

s = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
c = cairo.Context(s)

"""
# ctx.scale(width, height)  # Normalizing the canvas
# ctx.translate(0.1, 0.1)  # Changing the current transformation matrix
ctx.move_to(0, 0)
# Arc(cx, cy, radius, start_angle, stop_angle)
ctx.arc(2, 1, 1, -math.pi / 2, 0)
ctx.line_to(5, 100)  # Line to (x,y)
# Curve(x1, y1, x2, y2, x3, y3)
ctx.curve_to(5, 0.2, 0.5, 0.4, 0.2, 0.8)
ctx.close_path()

ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
ctx.set_line_width(0.02)
ctx.stroke()
"""


def draw_background(c, color, w, h):
    c.set_source_rgb(*color)
    c.rectangle(0, 0, w, h)
    c.fill()


def draw_arc(c, color, origin, theta_1, theta_2, r, width):
    c.set_source_rgb(*color)
    c.set_line_width(width)
    c.arc(origin[0], origin[1], r, theta_1, theta_2)
    c.stroke()


def draw_circle(c, color, origin, r, width):
    draw_arc(c, color, origin, 0, 2 * math.pi, r, width)


def draw_line(c, color, p1, p2, width):
    c.set_source_rgb(*color)
    c.set_line_width(width)
    c.move_to(*p1)
    c.line_to(*p2)
    c.stroke()


draw_background(c, bg, w, h)


# for r in range(0, width , incr):
#    draw_arc(c, (1, 1, 1), center, t1, t2, r, 0.2)


def draw_arc_lines(center, t1, t2, incr):
    for _ in range(0, 100):
        for r in range(0, width - incr, incr):
            for segment in range(0, math.floor(r / 10)):
                theta = t1 + (random.gauss(t2, pi))
                start = center[0] + r * sin(theta), center[1] + r * cos(theta)
                end = center[0] + (r + incr) * sin(theta), center[1] + (r + incr) * cos(
                    theta
                )
                draw_line(c, (1, 1, 1), start, end, 0.2)


# draw_arc_lines((0, 0), 0, 2 * pi, 200)
# draw_arc_lines((w / 2, h / 2), 0, 2 * pi, 200)

white = (1, 1, 1)


collidables = []


def draw_grid(num_bars):
    for i in range(0, num_bars):
        if i % 2 == 0:
            continue

        i = i * width / num_bars

        start = (i, 0)
        end = (i, height)
        draw_line(c, white, start, end, 0.5)
        collidables.append((start, end))

        start = (0, i)
        end = (width, i)
        draw_line(c, white, start, end, 0.5)
        collidables.append((start, end))


def draw_ray(start, direction, length):
    end = start + np.array(direction) * length
    draw_line(c, white, start, end, 2)


def find_ray_collisions(start, direction, max_length):
    intersects = []
    for (p0, p1) in collidables:
        found = vector.intersect_ray_vector(start, direction, p0, p1)
        if len(found) > 0:
            # print("found", found[0])
            intersects.append(found[0])
    line_and_len = [(vector.dist(start, end), end) for end in intersects]
    # print("line_and_len 0", line_and_len)
    length_and_end = [
        (length, end) for (length, end) in line_and_len if length < max_length
    ]

    return length_and_end.sort(key=lambda x: x[0])


def draw_ray_with_collisions(start, direction, max_length):
    length_and_end = find_ray_collisions(start, direction, max_length)
    if len(length_and_end) > 0:
        end = length_and_end[0][1]
        draw_line(c, white, start, end, 2)


def starburst(start, radius, num_lines, draw_only_collisions=False):
    for i in range(0, num_lines):
        direction = (cos(2 * pi * i / num_lines), sin(2 * pi * i / num_lines))
        if draw_only_collisions:
            draw_ray_with_collisions(start, direction, radius)
        else:
            draw_ray(start, direction, radius)


# draw_grid(10)

# for i in range(0, 100):
#     starburst(
#         (int(random.uniform(0, width)), int(random.uniform(0, height))),
#         (random.uniform(10, 300)),
#         int(random.uniform(10, 100)),
#     )


# for i in range(0, 1000):
#     start = (int(random.uniform(0, width)), int(random.uniform(0, height)))
#     direction = vector.norm(np.array([random.uniform(0, 1), random.uniform(-1, 1)]))
#     max_length = 300
#     draw_ray_with_collisions(start, direction, max_length)
circle_origin = (100, 100)
circle_radius = 50
ray_origin = (100, 100)
ray_direction = (1, 0.25)

draw_circle(c, white, circle_origin, circle_radius, 2)
draw_ray(ray_origin, ray_direction, 300)
intersections = vector.intersect_circle(
    ray_origin, ray_direction, circle_origin, circle_radius
)
print(intersections)

if intersections:
    blue = (0, 0, 1)
    red = (1, 0, 0)
    draw_circle(c, blue, intersections[0], 1, 10)
    draw_circle(c, red, intersections[1], 1, 10)


if __name__ == "__main__":
    s.write_to_png("example.png")  # Output to PNG
    s.finish()
