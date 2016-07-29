from pyglet.gl import *

BOID_SIZE = 5

window = pyglet.window.Window()

vertices = [
        0, 0,
        window.width, 0,
        window.width, window.height]
vertices_gl = (GLfloat * len(vertices))(*vertices)

glEnableClientState(GL_VERTEX_ARRAY)
glVertexPointer(2, GL_FLOAT, 0, vertices_gl)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 2)

pyglet.app.run()
