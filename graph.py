from typing import Dict
from shapes import *
from geometry import *

class NodeStyle:
    def __init__(self, fontname: str, label: str, shape: Shape):
        self.fontname = fontname
        self.label = label
        self.shape = shape

class Node:
    def __init__(self, height: float, width: float, pos: Point,
                 style: NodeStyle, shape: Shape = None, label: str = None):
        self.height = height
        self.width = width
        self.pos = pos

        self.label = label or style.label
        if shape == None:
            self.shape = style.shape.clone(pos, width, label)
        else:
            self.shape = shape

        self.object = Circle(self.pos, self.width)
        self.incommingEdges = list()

    def moveTo(self, pos: Point):
        self.pos = pos
        self.shape.moveTo(pos)
        self.object = Circle(self.pos, self.width)

    def render(self, canvas: Canvas):
        self.shape.render(canvas)
        for edge in self.incommingEdges:
            edge.render(canvas)

    def edgeIntersectPoint(self, segment: Segment) -> Point:
        return self.object.intersect(segment)


class EdgeStyle:
    def __init__(self, fontname: str):
        self.fontname = fontname


class Edge:
    def __init__(self, origin: Node, dest: Node, label: str, lp: Point):
        self.origin = origin 
        self.dest = dest 
        self.label = label
        self.lp = lp
        pos = self.calculatePos()
        self.shape = Arrow(pos[0], pos[1], label)
        origin.incommingEdges.append(self)
        dest.incommingEdges.append(self)

    def calculatePos(self):
        if (self.origin == self.dest):
            return (self.origin.pos, self.origin.pos)
        line = Segment(self.origin.pos, self.dest.pos)
        start = self.origin.edgeIntersectPoint(line)[0] or self.origin.pos
        end = self.dest.edgeIntersectPoint(line)[0] or self.dest.pos
        return (start, end)
    
    def render(self, canvas: Canvas):
        posX, posY = self.calculatePos()
        self.shape.moveTo(posX, posY)
        self.shape.render(canvas)


class BoundingBox:
    def __init__(self, x0: float, y0: float, x1: float, y1: float):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

class Graph:
    def __init__(self, defaultNodeStyle: NodeStyle = None, defaultEdgeStyle: EdgeStyle = None,
                 boundingBox: BoundingBox = None, fontname: str = "", params: Dict[str, str] = dict(),
                 name: str = ""):
        self.defaultNodeStyle = defaultNodeStyle
        self.defaultEdgeStyle = defaultEdgeStyle
        self.boundingBox = boundingBox
        self.fontname = fontname
        self.params = params
        self.name = name
        self.nodes = dict() # dictionary of nodes: label -> Node
        self.edges = list() # list of edges

    def addNode(self, node: Node):
        self.nodes[node.label] = node

    def addEdge(self, edge: Edge):
        self.edges.append(edge)

    def setBoundingBox(self, boundingBox: BoundingBox):
        self.boundingBox = boundingBox

    def setFontname(self, fontname: str):
        self.fontname = fontname

    def setParams(self, params: Dict[str, str]):
        self.params = params

    def setDefaultNodeStyle(self, nodeStyle: NodeStyle):
        self.defaultNodeStyle = nodeStyle

    def setDefaultEdgeStyle(self, edgeStyle: EdgeStyle):
        self.defaultEdgeStyle = edgeStyle

