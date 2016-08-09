# -*- coding: utf-8 -*-

import math
from pyglet.gl import (
    glPushMatrix, glTranslatef, glBegin, glColor4f, glVertex2f, glEnd, glPopMatrix,
    GL_TRIANGLE_FAN)


class Attractor:

    def __init__(self, position=[100, 100], magnitude=15.0, color=[0.0, 1.0, 0.0, 0.5]):
        self.position = position
        self.magnitude = magnitude
        self.color = color

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], 0.0)

        glBegin(GL_TRIANGLE_FAN)
        glColor4f(*self.color)

        glVertex2f(0.0, 0.0)
        step = 10
        # render a circle for the attractor
        for i in range(0, 360 + step, step):
            glVertex2f(self.magnitude * math.sin(math.radians(i)),
                       (self.magnitude * math.cos(math.radians(i))))
        glEnd()

        glPopMatrix()
