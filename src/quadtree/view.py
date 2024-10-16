import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle, Circle
# import matplotlib.style as mplstyle
# mplstyle.use(['dark_background', 'ggplot', 'fast'])
# from quadtree import Quadtree, Point2d

class Visualizer:
    def __init__(self, data_lim=(-200, -200, 200, 200), 
                    rect_size=(50, 50), circle_radius=50,
                    window_size=(720, 720), DPI=90) -> None:
        self.controller = None
        self.fig = plt.figure(figsize=(window_size[0]/DPI, window_size[1]/DPI), dpi=DPI)
        # if self.is_3d:
            # self.ax = plt.subplot(projection='3d')
        # else:
        self.ax = plt.subplot()
        # self.tree.draw(self.ax)

        plt.tight_layout()

        self.rect_size = rect_size # w, h
        self.circle_radius = circle_radius
        self.data_lim = data_lim
        self.is_mouse_enter = False


        # self.found_points_circle = self.ax.scatter([], [], s=700, color="r", marker="o")
        self.found_points = None
        self.mouse_position = self.ax.scatter([], [], s=10, color='k')

        # self.found_points_box = self.ax.scatter([], [], 500, "r", "*")
        self.rect = None
        self.circle = None
        
        self.data_points = None
        self.data_rects = []


        # if isinstance(self.tree, Quadtree):
        self.ax.set_xlim(self.data_lim[0], self.data_lim[2])
        self.ax.set_ylim(self.data_lim[1], self.data_lim[3])
        self.ax.invert_yaxis()

    
        plt.connect('motion_notify_event', self.on_move)
        plt.connect('button_press_event', self.on_click)

    def set_controller(self, controller):
        self.controller = controller

    def draw_data_points(self, points):
        if len(points) != 0:
            if self.data_points is None:
                self.data_points = self.ax.scatter([], [], s=20, color='k')
            self.data_points.set_offsets(points)
        else:
            if self.found_points is not None:
                self.data_points.remove()
                self.data_points = None
        plt.draw()
    
    def draw_found_data_points(self, points):
        if len(points) != 0:
            if self.found_points is None:
                self.found_points = self.ax.scatter(
                    [], [], s=200, color="r", marker=".", facecolors="none", edgecolors='r', linewidth=1)
            self.found_points.set_offsets(points)
        else:
            if self.found_points is not None:
                # self.found_points.set_offsets(np.empty(2,))
                self.found_points.remove()
                self.found_points = None
        plt.draw()

    def draw_rects(self, rects):
        if len(rects) == self.data_rects:
            return True
        for data_rect in self.data_rects:
            data_rect.remove()
        self.data_rects.clear()

        for rect in rects:
            xmin, ymin, w, h, num_points = rect
            rect = Rectangle((xmin, ymin), w, h,
                                    edgecolor='red',
                                    facecolor='none',
                                    lw=1 if num_points > 0 else 0.1)
            self.ax.add_patch(rect)
            self.data_rects.append(rect)
        plt.draw()

    def draw_circle(self, cx, cy, radius):
        if self.circle is None:
            self.circle = Circle((cx, cy), radius, 
                                edgecolor='blue', lw=2, fill=False)
            self.ax.add_patch(self.circle)
        else:
            self.circle.set_center((cx, cy))
            self.circle.set_radius(radius)
        plt.draw()

    def draw_rect(self, cx, cy, w, h):
        if self.rect is None:
            self.rect = Rectangle((cx, cy), w, h,
                                edgecolor='red', facecolor='none', lw=2)
            self.ax.add_patch(self.rect)
        else:
            self.rect.set_bounds(cx, cy, w, h)
        plt.draw()

    def on_move(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            self.mouse_position.set_offsets([x, y])
            self.controller.query_circle(x, y, self.circle_radius)
            self.controller.query_rect(x, y, self.rect_size[0], self.rect_size[1])

            # if se lf.query_box_size is not None:
            #     cx, cy = x-self.query_box_size[0]/2, y-self.query_box_size[1]/2
            #     if self.rect is None:
            #         self.rect = Rectangle((cx, cy), self.query_box_size[0], self.query_box_size[1],
            #                             edgecolor='blue',
            #                             facecolor='none',
            #                             lw=2)
            #         self.ax.add_patch(self.rect)
            #     else:
            #         self.rect.set_xy((cx, cy))
    
        else:
            self.mouse_position.set_offsets(np.empty((2,)))
            if self.rect is not None:
                self.rect.remove()
                self.rect = None
            if self.circle is not None:
                self.circle.remove()
                self.circle = None
            self.controller.out_event()
        plt.draw()

    def on_click(self, event):
        if event.button is MouseButton.LEFT:
            x, y = event.xdata, event.ydata 
            self.controller.on_left_mouse_click(x, y, self.circle_radius)

        if event.button is MouseButton.RIGHT:
            self.controller.on_right_mouse_click()

    def run(self):
        plt.show()
