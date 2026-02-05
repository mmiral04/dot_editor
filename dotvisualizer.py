import re
from tkinter import Canvas
from typing import Dict, Tuple

from shapes import *
from gui import GUI
from geometry import Point, Segment, Circle

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

    def moveTo(self, pos: Point):
        self.pos = pos
        self.shape.moveTo(pos)

    def render(self, canvas: Canvas):
        self.shape.render(canvas)

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
        self.pos = self.calculatePos()
        self.shape = Arrow(self.pos[0], self.pos[1], label)

    def calculatePos(self):
        if (self.origin == self.dest):
            return (self.origin.pos, self.origin.pos)
        line = Segment(self.origin.pos, self.dest.pos)
        start = self.origin.edgeIntersectPoint(line)[0]
        end = self.dest.edgeIntersectPoint(line)[0]
        return (start, end)
    
    def render(self, canvas: Canvas):
        self.shape.render(canvas)


class BoundingBox:
    def __init__(self, x0: float, y0: float, x1: float, y1: float):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

class Graph:
    def __init__(self, defaultNodeStyle: NodeStyle = None, defaultEdgeStyle: EdgeStyle = None,
                 boundingBox: BoundingBox = None, fontname: str = "", params: Dict[str, str] = dict()):
        self.defaultNodeStyle = defaultNodeStyle
        self.defaultEdgeStyle = defaultEdgeStyle
        self.boundingBox = boundingBox
        self.fontname = fontname
        self.params = params
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




def findObjects():
    param_re = re.compile(r"(\w+)=\"?([^\"\s\!]*)\!?\"?(?:, )?")
    object_re = re.compile(r"\b(\w+)\s(?:\-> )?(\w*\s)?\[(.*?)\];")

    file = open("afdmanual.dot", "r")
    data = file.read().replace("(?<!\\)\n", "") # remove new line
    data = re.sub(r"\s+", r" ", data)    # remove extra spaces

    # extract name
    name, data = re.search(r"digraph\s(.*?)\s\{(.*?)\}", data).groups()

    graph = Graph() 
    for object in object_re.finditer(data):
        # parse graph
        if object.group(1) == "graph": 
            additionalParams = dict()
            for parameter in object.group(3).split(", "):
                paramname, value = param_re.search(parameter).groups()
                if paramname == "bb":
                    edges = value.split(",")
                    graph.setBoundingBox(BoundingBox(float(edges[0]), float(edges[1]),
                                                     float(edges[2]), float(edges[3])))
                elif paramname == "fontname":
                    graph.setFontname(value)
                else:
                    additionalParams[paramname] = value

            graph.setParams(additionalParams)

        # parse default node style
        elif object.group(1) == "node":
            fontname = ""
            label = ""
            shape = None
            for parameter in object.group(3).split(", "):
                paramname, value = param_re.search(parameter).groups()
                if paramname == "fontname":
                    fontname = value
                elif paramname == "label":
                    label = value
                elif paramname == "shape":
                    # TODO: hacer factoria
                    if value == "circle":
                        shape = CircleShape()
                    elif value == "doublecircle":
                        shape = DoubleCircleShape()
            graph.setDefaultNodeStyle(NodeStyle(fontname, label, shape))

        # parse default edge style
        elif object.group(1) == "edge":
            fontname = ""
            for parameter in object.group(3).split(", "):
                paramname, value = param_re.search(parameter).groups()
                if paramname == "fontname":
                    fontname = value
            graph.setDefaultEdgeStyle(EdgeStyle(fontname))

        # parse nodes
        elif object.group(2) == None:
            height, pos, shape, label, width = "", None, None, object.group(1), 0
            shape_aux = ""
            for parameter in object.group(3).split(", "):
                paramname, value = param_re.search(parameter).groups()
                if paramname == "height":
                    height = float(value) * 21
                elif paramname == "pos":
                    pos_aux = value.split(",")
                    pos = Point(float(pos_aux[0])/1.6 + 300, (1500 - float(pos_aux[1]))/1.6 + 75)
                elif paramname == "shape":
                    shape_aux = value
                elif paramname == "width":
                    width = float(value) * 21

            if shape_aux == "circle":
                shape = CircleShape(pos, width, label)
            elif shape_aux == "doublecircle":
                shape = DoubleCircleShape(pos, width, label)
            n = Node(height, width, pos, graph.defaultNodeStyle, shape, label)
            graph.addNode(n)

        # parse edges
        else:
            origin, dest, label, lp, pos = object.group(1).strip(), object.group(2).strip(), "", (), ""
            for parameter in object.group(3).split(", "):
                paramname, value = param_re.search(parameter).groups()
                if paramname == "label":
                    label = value
                elif paramname == "lp":
                    lp_aux = value.split(",")
                    lp = Point(float(lp_aux[0]), float(lp_aux[1]))
                elif paramname == "pos":
                    pos = value 
            graph.addEdge(Edge(graph.nodes[origin], graph.nodes[dest], label, lp))

    return graph


if __name__ == "__main__":
    graph = findObjects()
    GUI(graph).start()
