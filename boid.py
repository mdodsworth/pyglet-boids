import math
from pyglet.gl import *

_BOID_WIDTH = 20.0
_BOID_LENGTH = 30.0

class Boid:
    def __init__(self, 
            position=[100.0,100.0], 
            max_position=[850, 650], 
            direction=[0.0,0.0], 
            color=[1.0,1.0,1.0]):
        self.position = position
        self.max_position = max_position
        self.direction = direction
        self.color = color

    def __repr__(self):
        return "Boid: position={}, direction={}, color={}".format(position, direction, color)


    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], 0.0)
        glRotatef(math.degrees(math.atan2(self.direction[0], self.direction[1])), 0.0, 0.0, -1.0)

        glBegin(GL_TRIANGLES)
        glColor3f(*self.color)
        glVertex2f(-(_BOID_WIDTH/2), 0.0)
        glVertex2f(0.0, _BOID_LENGTH)
        glVertex2f(_BOID_WIDTH/2, 0.0)
        glEnd()

        glPopMatrix()

    def update(self, dt):
        for i, pos in enumerate(self.position):
            self.position[i] += dt * self.direction[i]
            if self.position[i] >= self.max_position[i]:
                self.position[i] = (self.position[i] % self.max_position[i]) - 50.0
