# -*- coding: utf-8 -*-

import math


def magnitude(x, y):
    return math.sqrt((x ** 2) + (y ** 2))


def dot(a, b):
    return sum(i * j for i, j in zip(a, b))


def angle_between(a, b):
    angle = math.degrees(math.acos(dot(a, b) / (magnitude(*a) * magnitude(*b))))
    return angle


def limit_magnitude(vector, max_magnitude, min_magnitude = 0.0):
    mag = magnitude(*vector)
    if mag > max_magnitude:
        normalizing_factor = max_magnitude / mag
    elif mag < min_magnitude:
        normalizing_factor = min_magnitude / mag
    else: return vector

    return [value * normalizing_factor for value in vector]
