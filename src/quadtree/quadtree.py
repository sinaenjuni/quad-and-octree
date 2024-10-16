import numpy as np
import numpy.linalg as la
from matplotlib.patches import Rectangle

class Point2d:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def distance_to(self, other):
        return la.norm(self - other)
    
    def __add__(self, other):
        self.x += other[0]
        self.y += other[1]
        return self
    
    def __sub__(self, other):
        return np.asarray([self.x - other.x, self.y - other.y])
    
    def __eq__(self, other):
        if isinstance(other, Point2d):
            return self.x == other.x and self.y == other.y
        return False
    
    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"


class Quadtree:
    def __init__(self, xmin, ymin, xmax, ymax, 
            depth=0, max_point=1, max_depth=3, name="Root") -> None:
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

        self.points = []
        self.max_point = max_point
        self.max_depth = max_depth
        self.depth = depth
        self.name = name
        self.is_leaf = True

        self.TL = None 
        self.TR = None
        self.BL = None
        self.BR = None

    def insert_data(self, point):        
        if self.is_leaf: # if it's not leaf node, go to next node
            if len(self.points) < self.max_point:
                self.points.append(point)
                return True
            else:
                if self.divide():
                    return self.insert_data(point)
                else:
                    return False
        else:
            if self.TL.is_inner(point):
                return self.TL.insert_data(point)
            elif self.TR.is_inner(point):
                return self.TR.insert_data(point)
            elif self.BL.is_inner(point):
                return self.BL.insert_data(point)
            elif self.BR.is_inner(point):
                return self.BR.insert_data(point)
        
        raise ValueError(f"Out of range value, {point}")
            
    def delete_data(self, point):
        if self.is_leaf: # if it's not leaf node, go to next node
            if point in self.points:
                self.points.remove(point)
                return True
            else:
                raise ValueError(f"Point, {point} is not found")
                return False
        else:
            if self.TL.is_inner(point) and self.TL.delete_data(point):
                self.merge()
                return True
            elif self.TR.is_inner(point) and self.TR.delete_data(point):
                self.merge()
                return True
            elif self.BL.is_inner(point) and self.BL.delete_data(point):
                self.merge()
                return True
            elif self.BR.is_inner(point) and self.BR.delete_data(point):
                self.merge()
                return True
        
    
        # if not self.is_inner(point):
        #     return False

        # if not self.is_leaf:
        #     if (self.TL.delete_data(point) or self.TR.delete_data(point) or
        #         self.BL.delete_data(point) or self.BR.delete_data(point)):
            
        #         self.merge()
        #         return True
            
        # if point in self.points:
        #     self.points.remove(point)
        #     return True

        # return False

    def is_inner(self, point):
        return (
            self.xmin <= point.x and 
            self.ymin <= point.y and 
            self.xmax >= point.x and 
            self.ymax >= point.y
        )
        # if (point.x > self.xmax or point.x < self.xmin or
        # point.y > self.ymax or point.y < self.ymin):
        # return False
        
        # De Morgan's laws
        # xmin <= x and x <= xmax, <=> xmin > x or x > xmax
        # ymin <= y and y <= ymax, <=> ymin > y or y < ymax
    
    def divide(self):
        depth = self.depth + 1
        if depth > self.max_depth:
            raise ValueError(f"Reach for max depth ({self.max_depth})")
            return False
        
        self.is_leaf = False
        xmid = (self.xmin + self.xmax) / 2
        ymid = (self.ymin + self.ymax) / 2

        self.TL = Quadtree(self.xmin, self.ymin, xmid, ymid, depth, self.max_point, self.max_depth, "TL") #00
        self.TR = Quadtree(xmid, self.ymin, self.xmax, ymid, depth, self.max_point, self.max_depth, "TR") #01 
        self.BL = Quadtree(self.xmin, ymid, xmid, self.ymax, depth, self.max_point, self.max_depth, "BL") #10
        self.BR = Quadtree(xmid, ymid, self.xmax, self.ymax, depth, self.max_point, self.max_depth, "BR") #11

        for point in self.points:
            self.insert_data(point)
        self.points.clear()
        return True

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

    def query_rect(self, cx, cy, w, h, found_points):
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
            self.TL.query_rect(cx, cy, w, h, found_points)
            self.TR.query_rect(cx, cy, w, h, found_points)
            self.BL.query_rect(cx, cy, w, h, found_points)
            self.BR.query_rect(cx, cy, w, h, found_points)

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
                point.distance_to(Point2d(cx, cy)) <= radius):
                found_points.append(point)

        if not self.is_leaf:
            self.TL.query_circle(cx, cy, radius, found_points)
            self.TR.query_circle(cx, cy, radius, found_points)
            self.BL.query_circle(cx, cy, radius, found_points)
            self.BR.query_circle(cx, cy, radius, found_points)
        return found_points
    

    def update(self, old_point, new_point):        
        if self.delete_data(old_point):
            if self.insert_data(new_point):
                return True
            else:
                print(f"Error: Cannot insert {new_point}. Re-inserting {old_point}.")
                self.insert_data(old_point)
                return False
        else:
            print(f"Error: {old_point} not found.")
            return False
        
    def get_points(self):
        stack = [self] # retrieve tree using BFS
        ret = []
        while(len(stack) != 0):
            node = stack.pop(-1)
            points = node.points

            for point in points:
                ret.append(point)

            if not node.is_leaf:
                stack.append(node.BR)
                stack.append(node.BL)
                stack.append(node.TR)
                stack.append(node.TL)
        return ret
    
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
        stack = [self] # retrieve tree using BFS
        ret = ""
        while(len(stack) != 0):
            node = stack.pop(-1)
            points = node.points   

            ret += f"{"":>{node.depth * 6}} [{node.name} ({node.xmin}, {node.ymin} {node.xmax}, {node.ymax}){", Leaf" if node.is_leaf else ""}] "
            ret += f"{"-> " if len(node.points) != 0 else " "}" + ", ".join([str(point) for point in points]) + "\n"

            # if node.TL is not None and node.TR is not None and \
                # node.BL is not None and node.BR is not None:
            if not node.is_leaf:
                stack.append(node.BR)
                stack.append(node.BL)
                stack.append(node.TR)
                stack.append(node.TL)
        return ret
    
    def get_all_elements(self, rects, points):
        stack = [self]

        while(len(stack) != 0):
            node = stack.pop(-1)
            if node.is_leaf:
                points.append(node.points)
                rects.append([node.xmin, node.ymin, node.xmax, node.ymax])
            else:
                stack.append(node.BR)
                stack.append(node.BL)
                stack.append(node.TR)
                stack.append(node.TL)
            
    
    def draw(self, ax):
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin

        ax.add_patch(Rectangle((self.xmin, self.ymin), width, height,
                            edgecolor='red',
                            facecolor='none',
                            lw=4 if len(self.points) > 0 else 1))
        
        for point in self.points:
            ax.scatter(point.x, point.y, s=200, color='k')

        if self.TL is not None:
            self.TL.draw(ax)
        if self.TR is not None:
            self.TR.draw(ax)
        if self.BL is not None:
            self.BL.draw(ax)
        if self.BR is not None:
            self.BR.draw(ax)

if __name__ == "__main__":
    import time
    raw_data = np.random.rand(100000, 2) * 400 - 200
    model = Quadtree(-200, -200, 200, 200, 0, 10000, 5, "Root")

    s = time.time()
    points = []
    for x, y in raw_data:
        point = Point2d(x, y)
        ret = model.insert_data(point)
        points.append(point)
        # print(ret, point)
    e = time.time()
    print(e-s)

    s = time.time()
    for point in points:
        ret = model.delete_data(point)
        # print(ret)
    e = time.time()
    print(e-s)
