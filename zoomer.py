import pyglet
from pyglet.gl import gl
from pyglet.gl import glu
from pyglet.gl import Config


# colors
black = (0, 0, 0, 1)
green = (0, 1, 0)


def get_window_config():
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screen = display.get_default_screen()

    template = Config(double_buffer=1, sample_buffers=1, samples=4, stereo=1)

    try:
        config = screen.get_best_config(template)
    except pyglet.window.NoSuchConfigException:
        template = Config()
        config = screen.get_best_config(template)

    return config


window = pyglet.window.Window(width=300, height=300, caption='Zoom, pan and rotate', resizable=True, config=get_window_config())

class Square:
    def __init__(self, position=(0, 0, 0), color=green):
        (self.x, self.y, self.z) = position
        self.rx = self.ry = self.rz = 0
        self.color = color

    def draw(self):
        gl.glLoadIdentity()
        # position
        gl.glTranslatef(self.x, self.y, self.z)
        # rotation
        gl.glRotatef(self.rx, 1, 0, 0)
        gl.glRotatef(self.ry, 0, 1, 0)
        gl.glRotatef(self.rz, 0, 0, 1)
        # color
        gl.glColor3f(*self.color)
        # drawing
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex3f(1, 1, 0)
        gl.glVertex3f(-1, 1, 0)
        gl.glVertex3f(-1, -1, 0)
        gl.glVertex3f(1, -1, 0)
        gl.glEnd()


# background color
gl.glClearColor(*black)

square = Square((0, 0, -3))


@window.event
def on_resize(width, height):
    # sets the viewport
    gl.glViewport(0, 0, width, height)

    # sets the projection
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(60.0, width / float(height), 0.1, 100.0)

    # sets the model view
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
    # clears the background with the background color
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    # draws the square
    square.draw()


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    # scroll the MOUSE WHEEL to zoom
    square.z += scroll_y / 10.0


@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    # press the LEFT MOUSE BUTTON to rotate
    if button == pyglet.window.mouse.LEFT:
        square.ry -= dx / 5.0
        square.rx += dy / 5.0
    # press the LEFT and RIGHT MOUSE BUTTON simultaneously to pan
    if button == pyglet.window.mouse.LEFT | pyglet.window.mouse.RIGHT:
        square.x -= dx / 100.0
        square.y -= dy / 100.0


pyglet.app.run()
