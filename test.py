#!/usr/bin/env python
import cairo
import math
import random
from math import pi, sin, cos

width = w = 3508
height = h = 3508
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


draw_arc_lines((0, 0), 0, 2 * pi, 200)
draw_arc_lines((w / 2, h / 2), 0, 2 * pi, 200)


if __name__ == "__main__":
    s.write_to_png("example.png")  # Output to PNG
    s.finish()
