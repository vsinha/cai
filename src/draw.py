import math

import cairo
import numpy as np

width = w = 1500
height = h = w

s = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(s)


def background(color):
    ctx.set_source_rgb(*color)
    ctx.rectangle(0, 0, w, h)
    ctx.fill()


def arc(color, origin, theta_1, theta_2, r, width):
    ctx.set_source_rgb(*color)
    ctx.set_line_width(width)
    ctx.arc(origin[0], origin[1], r, theta_1, theta_2)
    ctx.stroke()


def circle(color, origin, r, width):
    arc(color, origin, 0, 2 * math.pi, r, width)


def line(color, p1, p2, width):
    ctx.set_source_rgb(*color)
    ctx.set_line_width(width)
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    ctx.stroke()


def grid(num_bars, color, collidables=None):
    for i in range(0, num_bars):
        # if i % 2 == 0:
        #     continue

        i = i * width / num_bars

        for (start, end) in [((i, 0), (i, height)), ((0, i), (width, i))]:
            line(color, start, end, 0.5)
            if collidables:
                collidables.add_line(start, end)


def ray(color, start, direction, length):
    end = start + np.array(direction) * length
    line(color, start, end, 2)


def ray_with_collisions(color, collidables, start, direction, max_length):
    length_and_end = collidables.ray_intersections(start, direction, max_length)
    if length_and_end and len(length_and_end) > 0:
        end = length_and_end[0][1]
        line(color, start, end, 2)


def starburst(color, collidables, start, radius, num_lines, draw_only_collisions=False):
    for i in range(0, num_lines):
        direction = (
            math.cos(2 * math.pi * i / num_lines),
            math.sin(2 * math.pi * i / num_lines),
        )
        if draw_only_collisions:
            ray_with_collisions(color, collidables, start, direction, radius)
        else:
            ray(start, direction, radius)
