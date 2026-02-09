import re
from tkinter import Canvas
from typing import Dict, Tuple

from parser import DotParser
from graph import *
from shapes import *
from gui import GUI
from geometry import Point

def writeObjects(graph: Graph):
    file = open("output.dot", "w")

    # header
    file.write(f"digraph {graph.name}" + " {\n")

    # graph section
    file.write("graph [layout = fdp, overlap = false];\n")

    # node section
    file.write('node [label = "\\N", shape=circle];\n')

    # edge section
    file.write('edge [fontname="Helvetica,Arial,sans-serif"];\n')

    # definitions
    for name, node in graph.nodes.items():
        file.write(f'{name} [shape={node.shape}, pos="{node.pos.x * 1.6},{(1500 - node.pos.y) *1.6}!"];\n')
    
    for edge in graph.edges:
        file.write(f'{edge.origin.label} -> {edge.dest.label} [label="{edge.label}"];\n')

    # end
    file.write("}")

if __name__ == "__main__":
    #graph = findObjects()
    graph = DotParser.parseFile("afdmanual2.dot")
    GUI(graph, writeObjects).start()
