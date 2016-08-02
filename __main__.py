from boid import Boid

import random
from pyglet.gl import *
from pyglet.window import key

boids = []

def random_boid(width, height):
    return Boid(
            position=[random.uniform(0, width), random.uniform(0,height)],
            direction=[random.uniform(-20.0, 20.0), random.uniform(-20.0, 20.0)],
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


def update(dt):
    for boid in boids:
        boid.update(dt)

def main():

    #window = pyglet.window.Window(config = get_window_config())
    window = pyglet.window.Window(
            800, 600,
            resizable=True,
            caption="Boids Simulation",
            config=get_window_config())

    for i in range(1, 100):
        boids.append(random_boid(window.width, window.height))

    # schedule world updates as often as possible
    pyglet.clock.schedule(update)

    @window.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        for boid in boids:
            boid.draw()


    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.Q and modifiers & key.MOD_COMMAND:
            pyglet.app.exit()
        elif symbol == key.EQUAL and modifiers & key.MOD_SHIFT:
            boids.append(random_boid(window.width, window.height))
        elif symbol == key.MINUS:
            boids.pop()

    pyglet.app.run()

main()
