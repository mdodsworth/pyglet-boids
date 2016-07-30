from pyglet.gl import *

BOID_WIDTH = 20
BOID_LENGTH = int(BOID_WIDTH * 1.2)

window = pyglet.window.Window()

# move this to somewhere useful
template = gl.Config(sample_buffers=1, samples=4)
try:
        config = screen.get_best_config(template)
except pyglet.window.NoSuchConfigException:
    template = gl.Config()
    config = screen.get_best_config(template)

window = pyglet.window.Window(config=config)

vertices = [
        0, 0,
        BOID_WIDTH, 0,
        BOID_WIDTH // 2, BOID_LENGTH]
vertices_gl = (GLfloat * len(vertices))(*vertices)

glEnableClientState(GL_VERTEX_ARRAY)
glVertexPointer(2, GL_FLOAT, 0, vertices_gl)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 2)

pyglet.app.run()
