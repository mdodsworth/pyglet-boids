import math
from pyglet.gl import *

_BOID_WIDTH = 20.0
_BOID_LENGTH = 30.0
_BOID_RANGE = 150.0
_BOUNDARY_SLOP = 200.0

class Boid:
    def __init__(self,
            position=[100.0,100.0],
            bounds=[1000, 1000],
            direction=[0.0,0.0],
            color=[1.0,1.0,1.0]):
        self.position = position
        self.bounds = bounds
        self.direction = direction
        self.color = color

    def __repr__(self):
        return "Boid: position={}, direction={}, color={}".format(position, direction, color)


    def render_direction(self):
        glColor3f(0.6, 0.6, 0.6)
        glBegin(GL_LINES)
        glVertex2f(0.0, _BOID_LENGTH)
        glVertex2f(0.0, _BOID_LENGTH + _BOID_RANGE)
        glEnd()


    def render_range(self):
        glColor3f(0.6, 0.1, 0.1)
        glBegin(GL_LINE_LOOP)
        # render a circle for the boid's range
        for i in range(0, 360, 20):
            glVertex2f(_BOID_RANGE * math.sin(math.radians(i)),
                (_BOID_RANGE * math.cos(math.radians(i))) + _BOID_LENGTH)
        glEnd()


    def render_boid(self):
        glBegin(GL_TRIANGLES)
        glColor3f(*self.color)
        glVertex2f(-(_BOID_WIDTH/2), 0.0)
        glVertex2f(0.0, _BOID_LENGTH)
        glVertex2f(_BOID_WIDTH/2, 0.0)
        glEnd()


    def draw(self, show_direction=False, show_range=False):
        glPushMatrix()

        # apply the transformation for the boid
        glTranslatef(self.position[0], self.position[1], 0.0)
        glRotatef(math.degrees(math.atan2(self.direction[0], self.direction[1])), 0.0, 0.0, -1.0)

        # render the boid's direction
        if show_direction:
            self.render_direction()

        # render the boid's range
        if show_range:
            self.render_range()

        # render the boid itself
        self.render_boid()
        glPopMatrix()

    def update(self, dt, other_boids):

        if self.position[0] < 0:
            print(self.position)

        # update the boid's direction based on several behavioural rules
        # take the average position of all the boids, and move the boid towards that point
        sum_x, sum_y = 0.0, 0.0
        for boid in other_boids:
            if boid != self:
                sum_x += boid.position[0]
                sum_y += boid.position[1]

        average_x, average_y = (sum_x / (len(other_boids) - 1), sum_y / (len(other_boids) - 1))

        for i, pos in enumerate(self.position):
            self.position[i] += dt * self.direction[i]
            if self.position[i] >= self.bounds[i] + _BOUNDARY_SLOP:
                self.position[i] = (self.position[i] % self.bounds[i]) - _BOUNDARY_SLOP
            elif self.position[i] <= -_BOUNDARY_SLOP:
                self.position[i] = self.bounds[i] + _BOUNDARY_SLOP
