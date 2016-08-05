import math
from pyglet.gl import *

_BOID_WIDTH = 20.0
_BOID_LENGTH = 30.0
_BOID_RANGE = 250.0
_BOID_VIEW_ANGLE = 110
_COLLISION_DISTANCE = 100.0
_CHANGE_VECTOR_LENGTH = 15.0
_MAX_SPEED = 150.0
_MIN_SPEED = 35.0
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
        self.change_vectors = []
        self.average_x, self.average_y = 0.0, 0.0

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


    def render_change_vectors(self):
        glBegin(GL_LINES)

        color = [0.0, 0.0, 0.0]
        for i, (factor, vector) in enumerate(self.change_vectors):
            #if i == 0:
                #print(*vector)
            color[i] = 1.0
            glColor3f(*color)
            glVertex2f(0.0, 0.0)
            glVertex2f(*[i * factor * _CHANGE_VECTOR_LENGTH for i in vector])
            color[i] = 0.0
        glEnd()


    def render_boid(self):
        glBegin(GL_TRIANGLES)
        glColor3f(*self.color)
        glVertex2f(-(_BOID_WIDTH/2), 0.0)
        glVertex2f(0.0, _BOID_LENGTH)
        glVertex2f(_BOID_WIDTH/2, 0.0)
        glEnd()


    def draw(self, show_velocity=False, show_view=False, show_vectors=False):
        glPushMatrix()
        # apply the transformation for the boid
        glTranslatef(self.position[0], self.position[1], 0.0)
        if show_vectors:
            self.render_change_vectors()

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
        return angle


    def limit_velocity(self):
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
            diff = (boid.position[0] - self.position[0], boid.position[1] - self.position[1])
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

            self.average_x, self.average_y = (sum_x / len(nearby_boids), sum_y / len(nearby_boids))
            return [self.average_x - self.position[0], self.average_y - self.position[1]]
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


    def avoid_collisions(self, boids):
        # determine nearby boids using distance only
        nearby_boids = (boid for boid in boids if (boid != self and
            self.vector_magnitude(boid.position[0] - self.position[0],
                boid.position[1] - self.position[1]) <= _COLLISION_DISTANCE))

        c = [0.0, 0.0]
        for boid in nearby_boids:
            c[0] = c[0] - (_COLLISION_DISTANCE / (boid.position[0] - self.position[0]))
            c[1] = c[1] - (_COLLISION_DISTANCE / (boid.position[1] - self.position[1]))

        return c


    def update(self, dt, all_boids):
        nearby_boids = list(self.determine_nearby_boids(all_boids))

        # update the boid's direction based on several behavioural rules
        cohesion_vector = self.direction_to_center(nearby_boids)
        alignment_vector = self.average_velocity(nearby_boids)
        separation_vector = self.avoid_collisions(all_boids)

        self.change_vectors = [
                (0.02, cohesion_vector),
                (0.02, alignment_vector),
                (0.05, separation_vector)]

        for factor, vector in self.change_vectors:
            self.velocity[0] += factor * vector[0]
            self.velocity[1] += factor * vector[1]

        # ensure that the boid's velocity is <= _MAX_SPEED
        self.limit_velocity()

        # move the boid to its new position, given its current velocity,
        # taking into account the world boundaries
        for i, pos in enumerate(self.position):
            self.position[i] += dt * self.velocity[i]
            if self.position[i] >= self.wrap_bounds[i]:
                self.position[i] = (self.position[i] % self.wrap_bounds[i]) - _BOUNDARY_SLOP
            elif self.position[i] < -_BOUNDARY_SLOP:
                self.position[i] = self.position[i] + self.wrap_bounds[i] + _BOUNDARY_SLOP
