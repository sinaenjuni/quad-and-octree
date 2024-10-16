import numpy as np
from matplotlib.backend_bases import MouseButton
from quadtree import Point2d

class Controller:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view
        self.view.set_controller(self)

        self.found_points = []
    
    def insert_data(self, x, y):
        ret = self.model.insert_data(Point2d(x, y))
        self.draw_rects_and_points()
        return ret

    def on_left_mouse_click(self, x, y, circle_radius):
        ret = self.insert_data(x, y)
        if ret:
            self.query_circle(x, y, circle_radius)

    def on_right_mouse_click(self):
        if len(self.found_points) != 0:
            self.delete_data()

    def draw_rects_and_points(self):
        rects, points = [], []
        self.model.get_all_elements(rects, points)
        # print(len(rects), len(points))
        # print(dir(self.view.data_points))
        # self.view.draw_points(points)
        rects_view, points_view = [], []
        for rect, point in zip(rects, points):
            xmin, ymin, xmax, ymax = rect
            w = xmax - xmin
            h = ymax - ymin
            num_points = len(point)
            rects_view.append([xmin, ymin, w, h, num_points])
            for p in point:
                points_view.append(np.asarray([p.x, p.y]))
        self.view.draw_data_points(points_view)
        self.view.draw_rects(rects_view)
        # print(self.model)

    

    def delete_data(self):
        for found_point in self.found_points:
            self.model.delete_data(found_point)
        self.draw_rects_and_points()
        self.view.draw_found_data_points([])
        # print(found_points)

    def query_circle(self, x, y, radius):
        self.view.draw_circle(x, y, radius)

        self.found_points = []
        self.model.query_circle(x, y, radius, self.found_points)
        self.view.draw_found_data_points(
            np.array([[p.x, p.y] for p in self.found_points]))
        
        # print(self.found_points)
        # for p in self.found_points:
            # print(p.x, p.y)
        # if event.button is MouseButton.RIGHT:
    
    def out_event(self):
        self.view.draw_found_data_points([])