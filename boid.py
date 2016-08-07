import math
import vector

from pyglet.gl import *

_BOID_RANGE = 250.0
_BOID_VIEW_ANGLE = 110
_BOID_COLLISION_DISTANCE = 45.0
_OBSTACLE_COLLISION_DISTANCE = 250.0
_MAX_COLLISION_VELOCITY = 1.0
_CHANGE_VECTOR_LENGTH = 15.0
_MAX_SPEED = 150.0
_MIN_SPEED = 25.0
_BOUNDARY_SLOP = 50.0

_COHESION_FACTOR = 0.03
_ALIGNMENT_FACTOR = 0.045
_BOID_AVOIDANCE_FACTOR = 7.5
_OBSTACLE_AVOIDANCE_FACTOR = 200.0
_ATTRACTOR_FACTOR = 0.0035

class Boid:
    def __init__(self,
            position=[100.0,100.0],
            bounds=[1000, 1000],
            velocity=[0.0,0.0],
            size=10.0,
            color=[1.0,1.0,1.0]):
        self.position = position
        self.wrap_bounds = [i + _BOUNDARY_SLOP for i in bounds]
        self.velocity = velocity
        self.size = size
        self.color = color
        self.change_vectors = []

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
            color[i % 3] = 1.0
            glColor3f(*color)
            glVertex2f(0.0, 0.0)
            glVertex2f(*[i * factor * _CHANGE_VECTOR_LENGTH for i in vector])
            color[i % 3] = 0.0
        glEnd()


    def render_boid(self):
        glBegin(GL_TRIANGLES)
        glColor3f(*self.color)
        glVertex2f(-(self.size), 0.0)
        glVertex2f(self.size, 0.0)
        glVertex2f(0.0, self.size * 3.0)
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


    def determine_nearby_boids(self, all_boids):
        """Note, this can be done more efficiently if performed globally, rather than for each individual boid."""
        for boid in all_boids:
            diff = (boid.position[0] - self.position[0], boid.position[1] - self.position[1])
            if (boid != self and
                    vector.magnitude(*diff) <= _BOID_RANGE and
                    vector.angle_between(self.velocity, diff) <= _BOID_VIEW_ANGLE):
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
            return [average_x -self.position[0], average_y - self.position[1]]
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


    def avoid_collisions(self, objs, collision_distance):
        # determine nearby objs using distance only
        nearby_objs = (obj for obj in objs if (obj != self and
            vector.magnitude(obj.position[0] - self.position[0],
                obj.position[1] - self.position[1]) - self.size <= collision_distance))

        c = [0.0, 0.0]
        for obj in nearby_objs:
            diff = obj.position[0] - self.position[0], obj.position[1] - self.position[1]
            inv_sqr_magnitude = 1 / ((vector.magnitude(*diff) - self.size) ** 2)

            c[0] = c[0] - inv_sqr_magnitude * diff[0]
            c[1] = c[1] - inv_sqr_magnitude * diff[1]
        return vector.limit_magnitude(c, _MAX_COLLISION_VELOCITY)


    def attraction(self, attractors):
        # generate a vector that moves the boid towards the attractors
        a = [0.0, 0.0]
        if not attractors: return a

        for attractor in attractors:
            a[0] += attractor.position[0] - self.position[0]
            a[1] += attractor.position[1] - self.position[1]

        return a


    def update(self, dt, all_boids, attractors, obstacles):
        nearby_boids = list(self.determine_nearby_boids(all_boids))

        # update the boid's direction based on several behavioural rules
        cohesion_vector = self.direction_to_center(nearby_boids)
        alignment_vector = self.average_velocity(nearby_boids)
        attractor_vector = self.attraction(attractors)
        boid_avoidance_vector = self.avoid_collisions(all_boids, _BOID_COLLISION_DISTANCE)
        obstacle_avoidance_vector = self.avoid_collisions(obstacles, _OBSTACLE_COLLISION_DISTANCE)

        self.change_vectors = [
                (_COHESION_FACTOR, cohesion_vector),
                (_ALIGNMENT_FACTOR, alignment_vector),
                (_ATTRACTOR_FACTOR, attractor_vector),
                (_BOID_AVOIDANCE_FACTOR, boid_avoidance_vector),
                (_OBSTACLE_AVOIDANCE_FACTOR, obstacle_avoidance_vector)]

        for factor, vec in self.change_vectors:
            self.velocity[0] += factor *vec[0]
            self.velocity[1] += factor *vec[1]

        # ensure that the boid's velocity is <= _MAX_SPEED
        self.velocity = vector.limit_magnitude(self.velocity, _MAX_SPEED, _MIN_SPEED)

        # move the boid to its new position, given its current velocity,
        # taking into account the world boundaries
        for i, pos in enumerate(self.position):
            self.position[i] += dt * self.velocity[i]
            if self.position[i] >= self.wrap_bounds[i]:
                self.position[i] = (self.position[i] % self.wrap_bounds[i]) - _BOUNDARY_SLOP
            elif self.position[i] < -_BOUNDARY_SLOP:
                self.position[i] = self.position[i] + self.wrap_bounds[i] + _BOUNDARY_SLOP
