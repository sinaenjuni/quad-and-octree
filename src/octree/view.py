import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import numpy as np

class Visualizer:
    def __init__(self, data_lim=(-200, -200, -200, 200, 200, 200), 
                    query_box_size=(50, 50), circle_radius=50,
                    window_size=(720, 720), DPI=100) -> None:
        self.controller = None
        self.fig = plt.figure(figsize=(window_size[0]/DPI, window_size[1]/DPI), dpi=DPI)
        self.ax = plt.subplot(projection='3d')

        plt.tight_layout()

        self.query_box_size = query_box_size # w, h
        self.circle_radius = circle_radius
        self.data_lim = data_lim
        self.is_mouse_enter = False


        # self.found_points_circle = self.ax.scatter([], [], s=700, color="r", marker="o")
        self.found_points = None
        self.mouse_position = self.ax.scatter([], [], [], s=100, color='k')

        # self.found_points_box = self.ax.scatter([], [], 500, "r", "*")
        self.found_box = None
        self.circle = None
        
        self.data_points = None
        self.data_rects = []


        self.ax.set_xlim(self.data_lim[0], self.data_lim[3])
        self.ax.set_ylim(self.data_lim[1], self.data_lim[4])
        self.ax.set_zlim(self.data_lim[2], self.data_lim[5])
        self.ax.invert_yaxis()

        # plt.connect('motion_notify_event', self.on_move)
        # plt.connect('button_press_event', self.on_click)

    def set_controller(self, controller):
        self.controller = controller

    def draw_data_points(self, points):
        if len(points) != 0:
            if self.data_points is None:
                self.data_points = self.ax.scatter([], [], [], s=20, color='k')
                # self.data_points = self.ax.scatter(points[:,0], points[:,1], points[:,2], s=200, color='k')
            self.data_points._offsets3d = (points[:,0], points[:,1], points[:,2])
        else:
            if self.found_points is not None:
                self.data_points.remove()
                self.data_points = None
        plt.draw()
    
    def draw_found_data_points(self, points):
        if len(points) != 0:
            if self.found_points is None:
                self.found_points = self.ax.scatter(
                    [], [], [], s=700, color="r", marker="o", facecolors="none", edgecolors='r', linewidth=4)
            self.found_points._offsets3d = (points[:,0], points[:,1], points[:,2])
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
            verts, num_points = rect
            rect = Poly3DCollection(verts, 
                                    linewidths=1 if num_points > 0 else 0.1,
                                    edgecolors='r', alpha=.01)
            self.ax.add_collection3d(rect)
            self.data_rects.append(rect)
        plt.draw()

    def draw_circle(self, x, y, z, radius):
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 30)

        x = x + radius * np.outer(np.cos(u), np.sin(v))
        y = y + radius * np.outer(np.sin(u), np.sin(v))
        z = z + radius * np.outer(np.ones(np.size(u)), np.cos(v))
        if self.circle is not None:
            self.circle.remove()
            self.circle = None
        self.circle = self.ax.plot_wireframe(x, y, z, color=(0, 0, 1, 0.3))
        plt.draw()

    def on_move(self, event):
        if event.inaxes:
            print(dir(event))
            x, y = event.xdata, event.ydata
            inv = self.ax.transData.inverted()
            ax_coords = inv.transform([x, y])
            print(ax_coords)

            # self.mouse_position.set_offsets([x, y, z])
            # self.controller.query_circle(x, y, self.circle_radius)

            # if se lf.query_box_size is not None:
            #     cx, cy = x-self.query_box_size[0]/2, y-self.query_box_size[1]/2
            #     if self.found_box is None:
            #         self.found_box = Rectangle((cx, cy), self.query_box_size[0], self.query_box_size[1],
            #                             edgecolor='blue',
            #                             facecolor='none',
            #                             lw=2)
            #         self.ax.add_patch(self.found_box)
            #     else:
            #         self.found_box.set_xy((cx, cy))
    
        else:
            self.mouse_position.set_offsets(np.empty((2,)))
            if self.found_box is not None:
                self.found_box.remove()
                self.found_box = None
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



