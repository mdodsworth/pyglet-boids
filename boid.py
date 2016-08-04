import math
from pyglet.gl import *

_BOID_WIDTH = 20.0
_BOID_LENGTH = 30.0
_BOID_RANGE = 250.0
_BOID_VIEW_ANGLE = 10
_MAX_SPEED = 100.0
_MIN_SPEED = 25.0
_BOUNDARY_SLOP = 200.0


class Boid:
    def __init__(self,
            position=[100.0,100.0],
            bounds=[1000, 1000],
            velocity=[0.0,0.0],
            color=[1.0,1.0,1.0]):
        self.position = position
        self.wrap_bounds = [i + _BOUNDARY_SLOP for i in bounds]
        self.velocity = velocity
        self.color = color

    def __repr__(self):
        return "Boid: position={}, velocity={}, color={}".format(self.position, self.velocity, self.color)


    def render_velocity(self):
        glColor3f(0.6, 0.6, 0.6)
        glBegin(GL_LINES)
        glVertex2f(0.0, 0.0)
        glVertex2f(0.0, _BOID_RANGE)
        glEnd()


    def render_view(self):
        glColor3f(0.6, 0.1, 0.1)
        glBegin(GL_LINE_LOOP)

        step = 10
        # render a circle for the boid's view
        for i in range(-_BOID_VIEW_ANGLE, _BOID_VIEW_ANGLE + step, step):
            glVertex2f(_BOID_RANGE * math.sin(math.radians(i)),
                (_BOID_RANGE * math.cos(math.radians(i))))
        glVertex2f(0.0, 0.0)
        glEnd()


    def render_boid(self):
        glBegin(GL_TRIANGLES)
        glColor3f(*self.color)
        glVertex2f(-(_BOID_WIDTH/2), 0.0)
        glVertex2f(0.0, _BOID_LENGTH)
        glVertex2f(_BOID_WIDTH/2, 0.0)
        glEnd()


    def draw(self, show_velocity=False, show_view=False):
        glPushMatrix()

        # apply the transformation for the boid
        glTranslatef(self.position[0], self.position[1], 0.0)
        glRotatef(math.degrees(math.atan2(self.velocity[0], self.velocity[1])), 0.0, 0.0, -1.0)

        # render the boid's velocity
        if show_velocity:
            self.render_velocity()

        # render the boid's view
        if show_view:
            self.render_view()

        # render the boid itself
        self.render_boid()
        glPopMatrix()


    def vector_magnitude(self, x, y):
        return math.sqrt((x ** 2) + (y ** 2))


    def vector_dot(self, a, b):
        return sum(i * j for i, j in zip(a, b))


    def vector_angle_between(self, a, b):
        angle = math.degrees(
                math.acos(self.vector_dot(a, b) / (self.vector_magnitude(*a) * self.vector_magnitude(*b))))
        print(angle)
        return angle


    def normalize_velocity(self):
        current_speed = self.vector_magnitude(*self.velocity)
        if current_speed > _MAX_SPEED:
            normalizing_factor = _MAX_SPEED / current_speed
        elif current_speed < _MIN_SPEED:
            normalizing_factor = _MIN_SPEED / current_speed
        else: return

        for i, value in enumerate(self.velocity):
            self.velocity[i] *= normalizing_factor


    def determine_nearby_boids(self, all_boids):
        """Note, this can be done more efficiently if performed globally, rather than for each individual boid."""
        for boid in all_boids:
            diff = (self.position[0] - boid.position[0], self.position[1] - boid.position[1])
            #print(self.vector_dot(self.velocity, diff) /
                    #(self.vector_magnitude(*self.velocity) * self.vector_magnitude(*diff)))
            if (boid != self and
                    self.vector_magnitude(*diff) <= _BOID_RANGE and
                    self.vector_angle_between(self.velocity, diff) <= _BOID_VIEW_ANGLE):
                yield boid
        return


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


    def average_velocity(self, nearby_boids):
        # take the average velocity of all nearby boids
        # todo - combine this function with direction_to_center
        if len(nearby_boids) > 0:
            sum_x, sum_y = 0.0, 0.0
            for boid in nearby_boids:
                sum_x += boid.velocity[0]
                sum_y += boid.velocity[1]

            average_x, average_y = (sum_x / len(nearby_boids), sum_y / len(nearby_boids))
            return [average_x - self.velocity[0], average_y - self.velocity[1]]
        else:
            return [0.0, 0.0]


    def update(self, dt, all_boids):
        nearby_boids = list(self.determine_nearby_boids(all_boids))

        # update the boid's direction based on several behavioural rules
        proximity_vector = self.direction_to_center(nearby_boids)
        velocity_vector = self.average_velocity(nearby_boids)

        change_vectors = [(0.01, proximity_vector), (0.01, velocity_vector)]
        for factor, vector in change_vectors:
            self.velocity[0] += factor * vector[0]
            self.velocity[1] += factor * vector[1]

        # ensure that the boid's velocity is <= _MAX_SPEED
        self.normalize_velocity()

        # move the boid to its new position, given its current velocity,
        # taking into account the world boundaries
        for i, pos in enumerate(self.position):
            self.position[i] += dt * self.velocity[i]
            if self.position[i] >= self.wrap_bounds[i]:
                self.position[i] = (self.position[i] % self.wrap_bounds[i]) - _BOUNDARY_SLOP
            elif self.position[i] < -_BOUNDARY_SLOP:
                self.position[i] = self.position[i] + self.wrap_bounds[i] + _BOUNDARY_SLOP
