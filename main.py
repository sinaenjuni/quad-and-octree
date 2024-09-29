import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle, Circle
import numpy as np
import time

from quadtree import QuadTree, Point

import matplotlib.style as mplstyle
mplstyle.use(['dark_background', 'ggplot', 'fast'])



class Visualizer:
    def __init__(self, tree=None, data_lim=(-200, -200, 200, 200), 
                    query_box_size=(50, 50), query_circle_radius=50,
                    window_size=(720, 720), DPI=50) -> None:
        self.mouse_position = None
        self.is_close = False
        self.data_lim = data_lim
        self.tree = tree

        # plt.ion()
        self.fig = plt.figure(figsize=(window_size[0]/DPI, window_size[1]/DPI), dpi=DPI)
        self.ax = plt.subplot()

        plt.connect('close_event', self.on_close)
        # plt.connect('figure_enter_event', self.enter_figure)
        # plt.connect('figure_leave_event', self.leave_figure)
        plt.connect('motion_notify_event', self.on_move)
        # plt.connect('button_press_event', on_click)

        plt.tight_layout()

        self.is_mouse_enter = False
        self.query_box_size = query_box_size # w, h
        self.query_circle_radius = query_circle_radius

        self.found_box = None # x, y, w, h
        self.found_circle = None #

    # def enter_figure(self, event):
    #     self.is_mouse_enter = True

    # def leave_figure(self, event):
    #     self.is_mouse_enter = False

    def on_move(self, event):
        if event.inaxes:
            self.is_mouse_enter = True
            self.mouse_position = np.array([event.xdata, event.ydata])
            # print(f'data coords {event.xdata} {event.ydata},',
                # f'pixel coords {event.x} {event.y}')
            self.found_box = (self.mouse_position[0]-self.query_box_size[0]/2,
                                self.mouse_position[1]-self.query_box_size[1]/2,
                                self.query_box_size[0],
                                self.query_box_size[1])
            
        else:
            self.is_mouse_enter = False
            self.qurey_box_size = None

    def on_close(self, event):
        if not self.is_close:
            self.is_close = True

    def on_click(self, event):
        if event.button is MouseButton.LEFT:
            pass
            # print('disconnecting callback')
            # plt.disconnect(binding_id)

    def run(self):
        while 1:
            # qt = QuadTree(0, 0, w, h, 2, 0)
            # points += (np.random.randn(n, 2) * 0.1)
            # for x, y in points:
            #     ret = qt.insert(Point(x, y))

            plt.cla()
            self.ax.set_xlim(self.data_lim[0], self.data_lim[2])
            self.ax.set_ylim(self.data_lim[1], self.data_lim[3])
            self.ax.invert_yaxis()

            if self.tree is not None:
                self.tree.draw(self.ax)

            # collisions = qt.detect_collisions(radius=2)
            # for p1, p2 in collisions:
            #     self.ax.scatter(p1.x, p1.y, 500, "r", "*")
            #     self.ax.scatter(p2.x, p2.y, 500, "r", "*")


            if self.is_mouse_enter == True:
                found_points = []
                qt.query_box(self.mouse_position[0], self.mouse_position[1],
                        self.query_box_size[0], self.query_box_size[1], found_points)
                
                for fount_point in found_points:
                    fount_point.color = 'r'
                #     self.ax.scatter(fount_point.x, fount_point.y, 500, "r", "*")
                    # print(fount_point, end=" ")
                # print()


                self.ax.scatter(self.mouse_position[0], self.mouse_position[1], 200)
                self.ax.add_patch(Rectangle((self.found_box[0], self.found_box[1]), 
                                            self.found_box[2], self.found_box[3],
                                    edgecolor='blue',
                                    facecolor='none',
                                    lw=1))
                self.ax.add_patch(Circle((self.mouse_position[0], self.mouse_position[1]), 
                                            self.query_circle_radius, fill=False))
            
            
            # qt.query_circle(mouse_position[0], mouse_position[1],
            #                 found_radius, found_points)

            
            plt.draw()
            # self.fig.canvas.flush_events()

            plt.pause(0.01)

            if self.is_close:
                break



import threading
def data_control_thread(qt, points):
    while 1:
        for point in points:
            qt.remove(point)
            # 포인트 좌표 업데이트
            point += np.random.randn(2, 1)
            qt.insert(point)
            # point += np.random.randn(2,1)
        time.sleep(0.2)
        # points += np.random.randn(20, 2)
        # print(points)

if __name__ == "__main__":
    # print(np.random.randn(20, 2))

    np.random.seed(123)

    data_lim = (-200, -200, 200, 200)
    n = 100

    qt = QuadTree(*data_lim, 4, 0)
    raw_data = (np.random.rand(n, 2) * max(data_lim) * 2) - 200
    # raw_data = [
    #     [10, 10],
    #     [15, 10],
    #     [10, 15],
    #     [120, 10]
    # ]
    # print(raw_data)

    points = []
    for x, y in raw_data:
        points.append(Point(x, y))
        ret = qt.insert(points[len(points)-1])
        # ret = qt.insert(Point(x, y))
        print(ret)
    # print(qt)q

    found_points = []
    qt.query_box( 0, 0, 160, 130, found_points)
    print(f"Found points in the box: {[str(p) for p in found_points]}")

    for found_point in found_points:
        ret = qt.remove(found_point)
        print(ret)
    # print(qt)

    # t1 = threading.Thread(target=data_control_thread, args=(qt, points,))
    # t1.daemon = True 
    # t1.start()

    vis = Visualizer(tree=qt, data_lim=data_lim)
    vis.run()





