import math
from pyglet.gl import *

_BOID_WIDTH = 20.0
_BOID_LENGTH = 30.0
_BOID_RANGE = 150.0
_MAX_SPEED = 75.0
_BOUNDARY_SLOP = 200.0


class Boid:
    def __init__(self,
            position=[100.0,100.0],
            bounds=[1000, 1000],
            direction=[0.0,0.0],
            color=[1.0,1.0,1.0]):
        self.position = position
        self.wrap_bounds = [i + _BOUNDARY_SLOP for i in bounds]
        self.direction = direction
        self.color = color

    def __repr__(self):
        return "Boid: position={}, direction={}, color={}".format(self.position, self.direction, self.color)


    def render_direction(self):
        glColor3f(0.6, 0.6, 0.6)
        glBegin(GL_LINES)
        glVertex2f(0.0, 0.0)
        glVertex2f(0.0, _BOID_RANGE)
        glEnd()


    def render_range(self):
        glColor3f(0.6, 0.1, 0.1)
        glBegin(GL_LINE_LOOP)
        # render a circle for the boid's range
        for i in range(0, 360, 20):
            glVertex2f(_BOID_RANGE * math.sin(math.radians(i)),
                (_BOID_RANGE * math.cos(math.radians(i))))
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

    def vector_magnitude(self, x, y):
        return math.sqrt((x ** 2) + (y ** 2))


    def normalize_direction(self):
        current_speed = self.vector_magnitude(*self.direction)
        if current_speed > _MAX_SPEED:
            normalizing_factor = _MAX_SPEED / current_speed
            for i, value in enumerate(self.direction):
                self.direction[i] *= normalizing_factor


    def determine_nearby_boids(self, all_boids):
        """Note, this can be done more efficiently if performed globally, rather than for each individual boid."""
        return (boid for boid in all_boids
                if self.vector_magnitude(
                    self.position[0] - boid.position[0],
                    self.position[1] - boid.position[1]) <= _BOID_RANGE
                and boid != self)


    def direction_to_center(self, nearby_boids):
        # take the average position of all nearby boids, and move the boid towards that point
        if len(nearby_boids) > 0:
            sum_x, sum_y = 0.0, 0.0
            for boid in nearby_boids:
                sum_x += boid.position[0]
                sum_y += boid.position[1]

            average_x, average_y = (sum_x / len(nearby_boids), sum_y / len(nearby_boids))
            return [average_x - self.position[0], average_y - self.position[1]]
        else:
            return [0.0, 0.0]


    def update(self, dt, all_boids):
        nearby_boids = list(self.determine_nearby_boids(all_boids))

        # update the boid's direction based on several behavioural rules
        proximity_vector = self.direction_to_center(nearby_boids)

        change_vectors = [(0.05, proximity_vector)]
        for factor, vector in change_vectors:
            self.direction[0] += factor * vector[0]
            self.direction[1] += factor * vector[1]

        # ensure that the boid's velocity is <= _MAX_SPEED
        self.normalize_direction()

        # move the boid to its new position, given its current direction,
        # taking into account the world boundaries
        for i, pos in enumerate(self.position):
            self.position[i] += dt * self.direction[i]
            if self.position[i] >= self.wrap_bounds[i]:
                self.position[i] = (self.position[i] % self.wrap_bounds[i]) - _BOUNDARY_SLOP
            elif self.position[i] < -_BOUNDARY_SLOP:
                self.position[i] = self.position[i] + self.wrap_bounds[i] + _BOUNDARY_SLOP
