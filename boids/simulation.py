# -*- coding: utf-8 -*-

import random
import pyglet
from pyglet.gl import (
    Config,
    glEnable, glBlendFunc, glLoadIdentity, glClear,
    GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT)
from pyglet.window import key

from .boid import Boid
from .attractor import Attractor
from .obstacle import Obstacle


def create_random_boid(width, height):
    return Boid(
        position=[random.uniform(0, width), random.uniform(0, height)],
        bounds=[width, height],
        velocity=[random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)],
        color=[random.random(), random.random(), random.random()])

def get_window_config():
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screen = display.get_default_screen()

    template = Config(double_buffer=True, sample_buffers=1, samples=4)
    try:
        config = screen.get_best_config(template)
    except pyglet.window.NoSuchConfigException:
        template = Config()
        config = screen.get_best_config(template)

    return config


def run():
    show_debug = False
    show_vectors = False
    boids = []
    attractors = []
    obstacles = []

    mouse_location = (0, 0)
    window = pyglet.window.Window(
        fullscreen=True,
        caption="Boids Simulation",
        config=get_window_config())

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #window.push_handlers(pyglet.window.event.WindowEventLogger())

    for i in range(1, 35):
        boids.append(create_random_boid(window.width, window.height))

    def update(dt):
        for boid in boids:
            boid.update(dt, boids, attractors, obstacles)

    # schedule world updates as often as possible
    pyglet.clock.schedule(update)

    @window.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        for boid in boids:
            boid.draw(show_velocity=show_debug, show_view=show_debug, show_vectors=show_vectors)

        for attractor in attractors:
            attractor.draw()

        for obstacle in obstacles:
            obstacle.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.Q:
            pyglet.app.exit()
        elif symbol == key.EQUAL and modifiers & key.MOD_SHIFT:
            boids.append(create_random_boid(window.width, window.height))
        elif symbol == key.MINUS and len(boids) > 0:
            boids.pop()
        elif symbol == key.D:
            nonlocal show_debug
            show_debug = not show_debug
        elif symbol == key.V:
            nonlocal show_vectors
            show_vectors = not show_vectors
        elif symbol == key.A:
            attractors.append(Attractor(position=mouse_location))
        elif symbol == key.O:
            obstacles.append(Obstacle(position=mouse_location))

    @window.event
    def on_mouse_drag(x, y, *args):
        nonlocal mouse_location
        mouse_location = x, y

    @window.event
    def on_mouse_motion(x, y, *args):
        nonlocal mouse_location
        mouse_location = x, y

    pyglet.app.run()
