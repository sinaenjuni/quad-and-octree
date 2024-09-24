import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import numpy as np

from quadtree import QuadTree, Point

mouse_position = (0,0)
def on_move(event):
    if event.inaxes:
        global mouse_position
        mouse_position = np.array([event.xdata, event.ydata])
        # print(f'data coords {event.xdata} {event.ydata},',
            # f'pixel coords {event.x} {event.y}')

is_close = False
def on_close(event):
    global is_close
    if not is_close:
        is_close = True

def on_click(event):
    if event.button is MouseButton.LEFT:
        pass
        # print('disconnecting callback')
        # plt.disconnect(binding_id)

if __name__ == "__main__":
    w, h = 200, 200
    n = 100
    points = np.random.rand(n, 2) * w

    DPI = 60
    fig = plt.figure(figsize=(1440/DPI, 720/DPI), dpi=DPI)
    ax = plt.subplot()

    plt.connect('close_event', on_close)
    binding_id = plt.connect('motion_notify_event', on_move)
    # plt.connect('button_press_event', on_click)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    plt.tight_layout()

    plt.ion() # turn interactive mode on
    while 1:
        qt = QuadTree(0, 0, w, h, 2, 0)
        points += (np.random.randn(n, 2) * 0.1)
        for x, y in points:
            ret = qt.insert(Point(x, y))

        plt.cla()
        ax.set_xlim(0, w)
        ax.set_ylim(0, h)
        ax.invert_yaxis()

        qt.draw(ax)

        ax.scatter(mouse_position[0], mouse_position[1], 200)
        plt.draw()
        plt.pause(0.01)

        if is_close:
            break

