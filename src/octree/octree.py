import numpy as np
import numpy.linalg as la
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Point3d:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return np.asarray([self.x - other.x, 
                            self.y - other.y,
                            self.z - other.z])
    
    def distance_to(self, other):
        return la.norm(self - other)
    
    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

class Octree:
    def __init__(self, xmin, ymin, zmin, xmax, ymax, zmax,
                    depth=0, max_point=1, max_depth=3, name="Root") -> None:
        self.xmin = xmin
        self.ymin = ymin
        self.zmin = zmin

        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax

        self.points = []
        self.max_point = max_point
        self.max_depth = max_depth
        self.depth = depth
        self.is_leaf = True
        self.name = name

        # self.children = [None for _ in range(8)]
        self.child_0 = None
        self.child_1 = None
        self.child_2 = None
        self.child_3 = None
        self.child_4 = None
        self.child_5 = None
        self.child_6 = None
        self.child_7 = None

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
            if self.child_0.is_inner(point):
                return self.child_0.insert_data(point)
            elif self.child_1.is_inner(point):
                return self.child_1.insert_data(point)
            elif self.child_2.is_inner(point):
                return self.child_2.insert_data(point)
            elif self.child_3.is_inner(point):
                return self.child_3.insert_data(point)
            elif self.child_4.is_inner(point):
                return self.child_4.insert_data(point)
            elif self.child_5.is_inner(point):
                return self.child_5.insert_data(point)
            elif self.child_6.is_inner(point):
                return self.child_6.insert_data(point)
            elif self.child_7.is_inner(point):
                return self.child_7.insert_data(point)
        
        raise ValueError(f"Out of range value, {point}")
        # if not self.is_inner(point):
        #     return False
        
        # if not self.is_leaf: # if it's not leaf node, go to next node
        #     if self.child_0.insert_data(point):
        #         return True
        #     if self.child_1.insert_data(point):
        #         return True
        #     if self.child_2.insert_data(point):
        #         return True
        #     if self.child_3.insert_data(point):
        #         return True
        #     if self.child_4.insert_data(point):
        #         return True
        #     if self.child_5.insert_data(point):
        #         return True
        #     if self.child_6.insert_data(point):
        #         return True
        #     if self.child_7.insert_data(point):
        #         return True
            
        # if len(self.points) < self.max_point:
        #     self.points.append(point)
        #     return True
        # else:
        #     if self.is_leaf:
        #         self.divide()
        #     return self.insert_data(point)
        
    def is_inner(self, point):
        return (self.xmin <= point.x and
                self.ymin <= point.y and
                self.zmin <= point.z and
                self.xmax >= point.x and 
                self.ymax >= point.y and
                self.zmax >= point.z
        )
    
    def divide(self):
        depth = self.depth + 1
        if depth > self.max_depth:
            raise ValueError(f"Reach for max depth ({self.max_depth})")
            return False

        self.is_leaf = False
        xmid = (self.xmin + self.xmax) / 2
        ymid = (self.ymin + self.ymax) / 2
        zmid = (self.zmin + self.zmax) / 2

        self.child_0 = Octree(self.xmin, self.ymin, self.zmin, 
                                xmid, ymid, zmid, 
                                depth, self.max_point, self.max_depth, "Child_0")
        self.child_1 = Octree(self.xmin, self.ymin, zmid,      
                                xmid, ymid, self.zmax, 
                                depth, self.max_point, self.max_depth, "Child_1")
        self.child_2 = Octree(self.xmin, ymid, self.zmin,      
                                xmid, self.ymax, zmid, 
                                depth, self.max_point, self.max_depth, "Child_2")
        self.child_3 = Octree(self.xmin, ymid, zmid,           
                                xmid, self.ymax, self.zmax, 
                                depth, self.max_point, self.max_depth, "Child_3")
        self.child_4 = Octree(xmid, self.ymin, self.zmin,      
                                self.xmax, ymid, zmid, 
                                depth, self.max_point, self.max_depth, "Child_4")
        self.child_5 = Octree(xmid, self.ymin, zmid,           
                                self.xmax, ymid, self.zmax, 
                                depth, self.max_point, self.max_depth, "Child_5")
        self.child_6 = Octree(xmid, ymid, self.zmin,           
                                self.xmax, self.ymax, zmid, 
                                depth, self.max_point, self.max_depth, "Child_6")
        self.child_7 = Octree(xmid, ymid, zmid,                
                                self.xmax, self.ymax, self.zmax, 
                                depth, self.max_point, self.max_depth, "Child_7")

        for point in self.points:
            self.insert_data(point)
        self.points.clear()
        # sections = [
        #     [self.xmin, self.ymin, self.zmin, xmid, ymid, zmid], # 000
        #     [self.xmin, self.ymin, zmid,      xmid, ymid, self.zmax], # 001
        #     [self.xmin, ymid, self.zmin,      xmid, self.ymax, zmid], # 010
        #     [self.xmin, ymid, zmid,           xmid, self.ymax, self.zmax], # 011
        #     [xmid, self.ymin, self.zmin,      self.xmax, ymid, zmid], # 100
        #     [xmid, self.ymin, zmid,           self.xmax, ymid, self.zmax], # 101
        #     [xmid, ymid, self.zmin,           self.xmax, self.ymax, zmid], # 110
        #     [xmid, ymid, zmid,                self.xmax, self.ymax, self.zmax], # 111
        # ]

        # for i in range(8):
        #     self.children[i] = Octree(*sections[i], self.max_point, depth, f"child_{i}")
        return True
    
    def delete_data(self, point):
        if self.is_leaf: # if it's not leaf node, go to next node
            if point in self.points:
                self.points.remove(point)
                return True
            else:
                raise ValueError(f"Point, {point} is not found")
                return False
        else:
            if self.child_0.is_inner(point) and self.child_0.delete_data(point):
                self.merge()
                return True
            elif self.child_1.is_inner(point) and self.child_1.delete_data(point):
                self.merge()
                return True
            elif self.child_2.is_inner(point) and self.child_2.delete_data(point):
                self.merge()
                return True
            elif self.child_3.is_inner(point) and self.child_3.delete_data(point):
                self.merge()
                return True
            elif self.child_4.is_inner(point) and self.child_4.delete_data(point):
                self.merge()
                return True
            elif self.child_5.is_inner(point) and self.child_5.delete_data(point):
                self.merge()
                return True
            elif self.child_6.is_inner(point) and self.child_6.delete_data(point):
                self.merge()
                return True
            elif self.child_7.is_inner(point) and self.child_7.delete_data(point):
                self.merge()
                return True
            
    def merge(self):
        if not self.is_leaf and\
            self.child_0.is_leaf and\
            self.child_1.is_leaf and\
            self.child_2.is_leaf and\
            self.child_3.is_leaf and\
            self.child_4.is_leaf and\
            self.child_5.is_leaf and\
            self.child_6.is_leaf and\
            self.child_7.is_leaf:

            if (len(self.child_0.points) + 
                len(self.child_1.points) + 
                len(self.child_2.points) + 
                len(self.child_3.points) + 
                len(self.child_4.points) + 
                len(self.child_5.points) + 
                len(self.child_6.points) + 
                len(self.child_7.points) <= self.max_point):
                
                self.points.extend(self.child_0.points)
                self.points.extend(self.child_1.points)
                self.points.extend(self.child_2.points)
                self.points.extend(self.child_3.points)
                self.points.extend(self.child_4.points)
                self.points.extend(self.child_5.points)
                self.points.extend(self.child_6.points)
                self.points.extend(self.child_7.points)

                self.child_0 = None
                self.child_1 = None
                self.child_2 = None
                self.child_3 = None
                self.child_4 = None
                self.child_5 = None
                self.child_6 = None
                self.child_7 = None
                self.is_leaf = True

    def query_circle(self, cx, cy, cz, radius, found_points):
        xmin = cx - radius
        xmax = cx + radius
        ymin = cy - radius
        ymax = cy + radius
        zmin = cz - radius
        zmax = cz + radius

        if (xmax < self.xmin or 
            xmin > self.xmax or
            ymax < self.ymin or 
            ymin > self.ymax or 
            zmax < self.zmin or 
            zmin > self.zmax):
            return False

        for point in self.points:
            if (xmin <= point.x and point.x <= xmax and
                ymin <= point.y and point.y <= ymax and
                zmin <= point.z and point.z <= zmax and
                point.distance_to(Point3d(cx, cy, cz)) <= radius):
                found_points.append(point)

        if not self.is_leaf:
            self.child_0.query_circle(cx, cy, cz, radius, found_points)
            self.child_1.query_circle(cx, cy, cz, radius, found_points)
            self.child_2.query_circle(cx, cy, cz, radius, found_points)
            self.child_3.query_circle(cx, cy, cz, radius, found_points)
            self.child_4.query_circle(cx, cy, cz, radius, found_points)
            self.child_5.query_circle(cx, cy, cz, radius, found_points)
            self.child_6.query_circle(cx, cy, cz, radius, found_points)
            self.child_7.query_circle(cx, cy, cz, radius, found_points)
        return found_points

    def query_box(self, cx, cy, cz, w, h, d, found_points):
            txmin = cx - w/2
            txmax = cx + w/2
            tymin = cy - h/2
            tymax = cy + h/2
            tzmin = cz - d/2
            tzmax = cz + d/2

            if (txmax < self.xmin or\
                txmin > self.xmax or\
                tymax < self.ymin or\
                tymin > self.ymax or\
                tzmax < self.zmin or\
                tzmin > self.zmax):
                return False

            for point in self.points:
                if (txmin <= point.x and point.x <= txmax and
                    tymin <= point.y and point.y <= tymax and
                    tzmin <= point.z and point.z <= tzmax):
                    found_points.append(point)

            if not self.is_leaf:
                self.child_0.query_box(cx, cy, w, h, found_points)
                self.child_1.query_box(cx, cy, w, h, found_points)
                self.child_2.query_box(cx, cy, w, h, found_points)
                self.child_3.query_box(cx, cy, w, h, found_points)
                self.child_4.query_box(cx, cy, w, h, found_points)
                self.child_5.query_box(cx, cy, w, h, found_points)
                self.child_6.query_box(cx, cy, w, h, found_points)
                self.child_7.query_box(cx, cy, w, h, found_points)
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

    def draw(self, ax):
        box_points = np.array([[self.xmin, self.ymin, self.zmin],
                                [self.xmax, self.ymin, self.zmin],
                                [self.xmax, self.ymax, self.zmin],
                                [self.xmin, self.ymax, self.zmin],
                                [self.xmin, self.ymin, self.zmax],
                                [self.xmax, self.ymin, self.zmax],
                                [self.xmax, self.ymax, self.zmax],
                                [self.xmin, self.ymax, self.zmax],
                                ])
        
        verts = [
            [box_points[j] for j in [0, 1, 2, 3]],
            [box_points[j] for j in [4, 5, 6, 7]],
            [box_points[j] for j in [0, 1, 5, 4]],
            [box_points[j] for j in [2, 3, 7, 6]],
            [box_points[j] for j in [0, 3, 7, 4]],
            [box_points[j] for j in [1, 2, 6, 5]]
        ]

        # ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.01))
        rect = ax.add_collection3d(Poly3DCollection(verts, 
                                            linewidths=1 if len(self.points) > 0 else 0.1,
                                            edgecolors='r', alpha=.01))
        
        for point in self.points:
            ax.scatter(point.x, point.y, point.z, s=200, color='k')

        if not self.is_leaf:
            self.child_0.draw(ax)
            self.child_1.draw(ax)
            self.child_2.draw(ax)
            self.child_3.draw(ax)
            self.child_4.draw(ax)
            self.child_5.draw(ax)
            self.child_6.draw(ax)
            self.child_7.draw(ax)

    
    def get_all_elements(self, rects, points):
        stack = [self]

        while(len(stack) != 0):
            node = stack.pop(-1)
            if node.is_leaf:
                points.append(node.points)
                rects.append([node.xmin, node.ymin, node.zmin,
                            node.xmax, node.ymax, node.zmax])
            else:
                stack.append(node.child_7)
                stack.append(node.child_6)
                stack.append(node.child_5)
                stack.append(node.child_4)
                stack.append(node.child_3)
                stack.append(node.child_2)
                stack.append(node.child_1)
                stack.append(node.child_0)
            

    def get_points(self):
        stack = [self] # retrieve tree using BFS
        ret = []
        while(len(stack) != 0):
            node = stack.pop(-1)
            points = node.points

            for point in points:
                ret.append(point)

            if not node.is_leaf:
                stack.append(node.child_7)
                stack.append(node.child_6)
                stack.append(node.child_5)
                stack.append(node.child_4)
                stack.append(node.child_3)
                stack.append(node.child_2)
                stack.append(node.child_1)
                stack.append(node.child_0)
        return ret
        
    def __str__(self) -> str:
            stack = [self] # retrieve tree using BFS
            ret = ""
            while(len(stack) != 0):
                node = stack.pop(-1)
                points = node.points   

                ret += f"{"":>{node.depth * 6}} [{node.name} ({node.xmin}, {node.ymin}, {node.zmin}, {node.xmax}, {node.ymax}, {node.zmax}){", Leaf" if node.is_leaf else ""}] "
                ret += f"{"-> " if len(node.points) != 0 else " "}" + ", ".join([str(point) for point in points]) + "\n"

                if not node.is_leaf:
                    stack.append(node.child_7)
                    stack.append(node.child_6)
                    stack.append(node.child_5)
                    stack.append(node.child_4)
                    stack.append(node.child_3)
                    stack.append(node.child_2)
                    stack.append(node.child_1)
                    stack.append(node.child_0)
            return ret

def print_tree(root:Octree):
    stack = [root]

    while(len(stack) != 0):
        node = stack.pop(-1)
        points = node.points

        if node.child_0 is not None and node.child_1 is not None and\
            node.child_2 is not None and node.child_3 is not None and\
            node.child_4 is not None and node.child_5 is not None and \
            node.child_6 is not None and node.child_7 is not None:
            stack.append(node.child_0)
            stack.append(node.child_1)
            stack.append(node.child_2)
            stack.append(node.child_3)
            stack.append(node.child_4)
            stack.append(node.child_5)
            stack.append(node.child_6)
            stack.append(node.child_7)

        # ret = f"[{node_type:>{node.depth}}]"
        ret = f"{"":>{node.depth * 6}} [{node.name}{", Leaf" if node.is_leaf else ""}] "
        ret += ", ".join([str(point) for point in points])
        print(ret)


if __name__ == "__main__":
    import time
    raw_data = np.random.rand(1000000, 3) * 400 - 200
    model = Octree(-200, -200, -200, 200, 200, 200,
                depth=0, max_point=1000, max_depth=4, name="Root")

    s = time.time()
    points = []
    for x, y, z in raw_data:
        point = Point3d(x, y, z)
        points.append(point)
        ret = model.insert_data(point)
    e = time.time()
    print(e-s)

    s = time.time()
    for point in points:
        ret = model.delete_data(point)
        # print(ret)
    e = time.time()
    print(e-s)
