## shapely wrapper to simplify line and circle intersection

from typing import List, Tuple
import math

import shapely.geometry as sg


class Point:
    def __init__(self, x: float = None, y: float = None, pos: Tuple[int, int] = None):
        self.x = x or pos[0] or 0
        self.y = y or pos[1] or 0

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")" 
    
class Segment:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2
        self.object = sg.LineString([(p1.x, p1.y), (p2.x, p2.y)])
    
class Circle:
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius
        self.object = sg.Point(center.x, center.y).buffer(radius).boundary

    def intersect(self, segment: Segment) -> List[Point]:
        points = list()
        i = self.object.intersection(segment.object)
        if (type(self.object.intersection(segment.object)) == sg.point.Point):
            # single point
            points.append(Point(i.coords[0][0], i.coords[0][1]))
        else:
            # multiple points
            for p in self.object.intersection(segment.object).geoms:
                points.append(Point(p.coords[0][0], p.coords[0][1]))

        return points


if __name__ == "__main__":
    s = Segment(Point(-5, 5), Point(4, 1))
    c = Circle(Point(-5, 5), 2)
    c.intersect(s)