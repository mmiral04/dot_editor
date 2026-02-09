from abc import ABC, abstractmethod
import re

from geometry import Point
from shapes import CircleShape, DoubleCircleShape
from graph import *

class ParserInterface(ABC):
    @staticmethod
    @abstractmethod
    def parseFile(path: str) -> Graph:
        raise NotImplementedError

class DotParser(ParserInterface):
    param_re = re.compile(r"(\w+)=\"?([^\"\s\!]*)\!?\"?(?:, )?")
    object_re = re.compile(r"\b(\w+)\s(?:\-> )?(\w*\s)?\[(.*?)\];")

    @staticmethod
    def parseFile(path: str) -> Graph:
        file = open(path, "r")
        data = file.read().replace("(?<!\\)\n", "") # remove new line
        data = re.sub(r"\s+", r" ", data)           # remove extra spaces

        parsers = [DotParser.parseGraph, DotParser.parseNodeStyle, DotParser.parseEdgeStyle,
                   DotParser.parseNode, DotParser.parseEdge]

        # extract name
        name, data = re.search(r"digraph\s(.*?)\s\{(.*?)\}", data).groups()

        graph = Graph(name = name) 
        for object in DotParser.object_re.finditer(data):
            for p in parsers:
                if p(graph, object):
                    break

        return graph
    
    @staticmethod
    def parseGraph(graph: Graph, object: re.Match) -> bool:
        if object.group(1) == "graph":
            additionalParams = dict()
            for parameter in object.group(3).split(", "):
                paramname, value = DotParser.param_re.search(parameter).groups()
                if paramname == "bb":
                    edges = value.split(",")
                    graph.setBoundingBox(BoundingBox(float(edges[0]), float(edges[1]),
                                                    float(edges[2]), float(edges[3])))
                elif paramname == "fontname":
                    graph.setFontname(value)
                else:
                    additionalParams[paramname] = value
            graph.setParams(additionalParams)
            return True
        
        return False

    @staticmethod
    def parseNodeStyle(graph: Graph, object: re.Match) -> bool:
        if object.group(1) == "node":
            fontname = ""
            label = ""
            shape = None
            for parameter in object.group(3).split(", "):
                paramname, value = DotParser.param_re.search(parameter).groups()
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
            return True
        
        return False

    @staticmethod
    def parseEdgeStyle(graph: Graph, object: re.Match) -> bool:
        if object.group(1) == "edge":
            fontname = ""
            for parameter in object.group(3).split(", "):
                paramname, value = DotParser.param_re.search(parameter).groups()
                if paramname == "fontname":
                    fontname = value
            graph.setDefaultEdgeStyle(EdgeStyle(fontname))
            return True
        
        return False

    @staticmethod
    def parseNode(graph: Graph, object: re.Match) -> bool:
        if object.group(2) == None:
            height, pos, shape, label, width = "", None, None, object.group(1), 0
            shape_aux = ""
            for parameter in object.group(3).split(", "):
                paramname, value = DotParser.param_re.search(parameter).groups()
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
            return True
        
        return False

    @staticmethod
    def parseEdge(graph: Graph, object: re.Match) -> bool:
        if object.group(2) != None:
            origin, dest, label, lp, pos = object.group(1).strip(), object.group(2).strip(), "", (), ""
            for parameter in object.group(3).split(", "):
                paramname, value = DotParser.param_re.search(parameter).groups()
                if paramname == "label":
                    label = value
                elif paramname == "lp":
                    lp_aux = value.split(",")
                    lp = Point(float(lp_aux[0]), float(lp_aux[1]))
                elif paramname == "pos":
                    pos = value 
            graph.addEdge(Edge(graph.nodes[origin], graph.nodes[dest], label, lp))
            return True
        
        return False