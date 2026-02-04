import re
from typing import Tuple

from shapes import *
from gui import GUI

class NodeStyle:
    def __init__(self, fontname: str, label: str, shape: Shape):
        self.fontname = fontname
        self.label = label
        self.shape = shape

class Node:
    def __init__(self, height: float, width: float, pos: Tuple[float, float],
                 style: NodeStyle, shape: Shape = None, label: str = None):
        self.height = height
        self.width = width
        self.pos = pos
        # set default style
        self.label = style.label
        self.shape = style.shape

        # overwrite with specific style if defined
        self.label = label or self.label
        self.shape = shape or self.shape

    def moveTo(self, pos: Tuple[float, float]):
        self.pos = pos

    def render(self, canvas: Canvas):
        self.shape.render(canvas, self.pos, self.width/2, self.label)


class EdgeStyle:
    def __init__(self, fontname: str):
        self.fontname = fontname


class Edge:
    def __init__(self, origin: Node, dest: Node, label: str, lp: Tuple[int, int], pos: str):
        self.origin = origin 
        self.dest = dest 
        self.label = label
        self.lp = lp
        self.pos = pos


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


param_re = re.compile(r"(\w+)=\"?([^\"\s\!]*)\!?\"?(?:, )?")


def findObjects():
    file = open("afdmanual.dot", "r")
    data = file.read().replace("(?<!\\)\n", "") # remove new line
    data = re.sub(r"\s+", r" ", data)    # remove extra spaces

    # extract name
    name, data = re.search(r"digraph\s(.*?)\s\{(.*?)\}", data).groups()

    graph = Graph() 
    for object in re.finditer(r"\b(\w+)\s(?:\-> )?(\w*\s)?\[(.*?)\];", data):
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
            for parameter in object.group(3).split(", "):
                paramname, value = param_re.search(parameter).groups()
                if paramname == "height":
                    height = float(value) * 42
                elif paramname == "pos":
                    pos_aux = value.split(",")
                    pos = (float(pos_aux[0])/1.6 + 300, (1500 - float(pos_aux[1]))/1.6 + 75)
                elif paramname == "shape":
                    # TODO: factoria
                    if value == "circle":
                        shape = CircleShape()
                    elif value == "doublecircle":
                        shape = DoubleCircleShape()
                elif paramname == "width":
                    width = float(value) * 42
            graph.addNode(Node(height, width, pos, graph.defaultNodeStyle, shape, label))

        # parse edges
        else:
            origin, dest, label, lp, pos = object.group(1), object.group(2), "", (), ""
            for parameter in object.group(3).split(", "):
                paramname, value = param_re.search(parameter).groups()
                if paramname == "label":
                    label = value
                elif paramname == "lp":
                    lp_aux = value.split(",")
                    lp = (float(lp_aux[0]), float(lp_aux[1]))
                elif paramname == "pos":
                    pos = value 
            graph.addEdge(Edge(origin, dest, label, lp, pos))

    return graph


if __name__ == "__main__":
    graph = findObjects()
    GUI(graph).start()
