import numpy as np
from matplotlib.patches import Rectangle

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def distance_to(self, other):
        return np.hypot(*(self - other))
    
    def __add__(self, other):
        self.x += other[0]
        self.y += other[1]
    
    def __sub__(self, other):
        return np.array([self.x - other.x, self.y - other.y])
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False
    
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
        self.is_leaf = True
    
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
        self.is_leaf = False

        for point in self.points:
            self.insert(point)
        self.points.clear()

    def merge(self):
        if not self.is_leaf and self.TL.is_leaf and self.TR.is_leaf and self.BL.is_leaf and self.BR.is_leaf:
            if (len(self.TL.points) + len(self.TR.points) + 
                len(self.BL.points) + len(self.BR.points) <= self.max_point):
                
                self.points.extend(self.TL.points)
                self.points.extend(self.TR.points)
                self.points.extend(self.BL.points)
                self.points.extend(self.BR.points)

                self.TL = self.TR = self.BL = self.BR = None
                self.is_leaf = True

    def insert(self, point):
        if not self.is_inner(point):
            return False
        
        if not self.is_leaf: # if it's not leaf node, go to next node
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
            if self.is_leaf:
                self.divide()
            return self.insert(point)
        
    def remove(self, point):
        if (point.x > self.xmax or point.y > self.ymax or
            point.x < self.xmin or point.y < self.ymin):
            return False
        
        if not self.is_leaf:
            if (self.TL.remove(point) or self.TR.remove(point) or
                self.BL.remove(point) or self.BR.remove(point)):
                self.merge()
                return True
            
        if point in self.points:
            self.points.remove(point)
            return True

        return False
    
    def query_box(self, cx, cy, w, h, found_points):
        txmin = cx - w/2
        txmax = cx + w/2
        tymin = cy - h/2
        tymax = cy + h/2

        if (txmax < self.xmin or txmin > self.xmax or
                tymax < self.ymin or tymin > self.ymax):
            return False

        for point in self.points:
            if (txmin <= point.x and point.x <= txmax and
                tymin <= point.y and point.y <= tymax):
                found_points.append(point)

        if not self.is_leaf:
            self.TL.query_box(cx, cy, w, h, found_points)
            self.TR.query_box(cx, cy, w, h, found_points)
            self.BL.query_box(cx, cy, w, h, found_points)
            self.BR.query_box(cx, cy, w, h, found_points)

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

        if not self.is_leaf:
            self.TL.query_circle(cx, cy, radius, found_points)
            self.TR.query_circle(cx, cy, radius, found_points)
            self.BL.query_circle(cx, cy, radius, found_points)
            self.BR.query_circle(cx, cy, radius, found_points)
        return found_points
    
    def detect_collisions(self, radius):
        collisions = []
        self._detect_collisions_in_node(collisions, radius)
        return collisions

    def _detect_collisions_in_node(self, collisions, radius):
        for i, point1 in enumerate(self.points):
            for point2 in self.points[i+1:]:
                if point1.distance_to(point2) <= radius:
                    collisions.append((point1, point2))

        if not self.is_leaf:
            self.TL._detect_collisions_in_node(collisions, radius)
            self.TR._detect_collisions_in_node(collisions, radius)
            self.BL._detect_collisions_in_node(collisions, radius)
            self.BR._detect_collisions_in_node(collisions, radius)

    
    def __str__(self) -> str:
        ret = "{}, {} :: ".format(self.depth, self.is_leaf)
        # ret = "divide: {}\n".format(self.is_divide)
        # ret += "xmin: {}, ymin: {}, xmax: {}, ymax:{}\n".format(self.xmin, self.ymin, self.xmax, self.ymax)
        # ret += "depth: {}\n".format(self.depth)
        # ret += "points: \n"
        ret += " ".join([str(p) for p in self.points])
        if not self.is_leaf:
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
        
        for point in self.points:
            ax.scatter(point.x, point.y, s=200, color='k')

        if not self.is_leaf:
            self.TL.draw(ax)
            self.TR.draw(ax)
            self.BL.draw(ax)
            self.BR.draw(ax)
            