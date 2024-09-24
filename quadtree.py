import numpy as np
from matplotlib.patches import Rectangle

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def distance_to(self, other):
        return np.hypot(*(self - other))
    
    def __sub__(self, other):
        return np.array([self.x - other.x, self.y - other.y])
    
    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)

class QuadTree:
    def __init__(self, xmin, ymin, xmax, ymax, max_point=1, depth=0) -> None:
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

        self.max_point = max_point
        self.depth = depth
        self.points = []
        self.is_divide = False
    
    def is_inner(self, point):
        return (self.xmin <= point.x and point.x <= self.xmax and
                self.ymin <= point.y and point.y <= self.ymax)

    def divide(self):
        depth = self.depth + 1
        x_mid = (self.xmin + self.xmax) / 2
        y_mid = (self.ymin + self.ymax) / 2

        self.TL = QuadTree(self.xmin, self.ymin, x_mid, y_mid, self.max_point, depth)
        self.TR = QuadTree(x_mid, self.ymin, self.xmax, y_mid, self.max_point, depth)
        self.BL = QuadTree(self.xmin, y_mid, x_mid, self.ymax, self.max_point, depth)
        self.BR = QuadTree(x_mid, y_mid, self.xmax, self.ymax, self.max_point, depth)
        self.is_divide = True

        for point in self.points:
            if self.TL.insert(point):
                continue
            elif self.TR.insert(point):
                continue
            elif self.BL.insert(point):
                continue
            elif self.BR.insert(point):
                continue
        self.points.clear()

    def insert(self, point):
        if not self.is_inner(point):
            return False
        
        if self.is_divide:
            if self.TL.insert(point):
                return True
            elif self.TR.insert(point):
                return True
            elif self.BL.insert(point):
                return True
            elif self.BR.insert(point):
                return True

        if len(self.points) < self.max_point:
            self.points.append(point)
            return True
        else:
            if not self.is_divide:
                self.divide()
            if self.TL.insert(point):
                return True
            elif self.TR.insert(point):
                return True
            elif self.BL.insert(point):
                return True
            elif self.BR.insert(point):
                return True                    
        return -1
    
    def query(self, cx, cy, w, h, found_points):
        xmin = cx - w/2 
        xmax = cx + w/2 
        ymin = cy - h/2 
        ymax = cy + h/2 

        if (xmax < self.xmin or xmin > self.xmax or
            ymax < self.ymin or ymin > self.ymax):
            return False

        for point in self.points:
            if (xmin <= point.x and point.x <= xmax and
                ymin <= point.y and point.y <= ymax):
                found_points.append(point)

        if self.is_divide:
            self.TL.query(cx, cy, w, h, found_points)
            self.TR.query(cx, cy, w, h, found_points)
            self.BL.query(cx, cy, w, h, found_points)
            self.BR.query(cx, cy, w, h, found_points)
        return found_points
    
    def query_circle(self, cx, cy, radius, found_points):
        xmin = cx - radius
        xmax = cx + radius
        ymin = cy - radius
        ymax = cy + radius

        if (xmax < self.xmin or xmin > self.xmax or
            ymax < self.ymin or ymin > self.ymax):
            return False

        for point in self.points:
            if (xmin <= point.x and point.x <= xmax and
                ymin <= point.y and point.y <= ymax and
                point.distance_to(Point(cx, cy)) <= radius):
                found_points.append(point)

        if self.is_divide:
            self.TL.query_circle(cx, cy, radius, found_points)
            self.TR.query_circle(cx, cy, radius, found_points)
            self.BL.query_circle(cx, cy, radius, found_points)
            self.BR.query_circle(cx, cy, radius, found_points)
        return found_points
    
    def __str__(self) -> str:
        ret = "{}, {} :: ".format(self.depth, self.is_divide)
        # ret = "divide: {}\n".format(self.is_divide)
        # ret += "xmin: {}, ymin: {}, xmax: {}, ymax:{}\n".format(self.xmin, self.ymin, self.xmax, self.ymax)
        # ret += "depth: {}\n".format(self.depth)
        # ret += "points: \n"
        ret += " ".join([str(p) for p in self.points])
        if self.is_divide:
            print(self.TL)
            print(self.TR)
            print(self.BL)
            print(self.BR)
        return ret
    
    def draw(self, ax):
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin

        ax.add_patch(Rectangle((self.xmin, self.ymin), width, height,
                            edgecolor='red',
                            facecolor='none',
                            lw=4 if len(self.points) > 0 else 1))
        
        for p in self.points:
                ax.scatter(p.x, p.y, s=200, color='blue')

        if self.is_divide:
            self.TL.draw(ax)
            self.TR.draw(ax)
            self.BL.draw(ax)
            self.BR.draw(ax)
            