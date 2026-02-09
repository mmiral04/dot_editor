from abc import ABC, abstractmethod

from graph import *
import svg
from textwrap import dedent


class WriterInterface(ABC):
    @staticmethod
    @abstractmethod
    def write(graph: Graph, path: str):
        raise NotImplementedError
    
class DotWriter(WriterInterface):
    @staticmethod
    def write(graph: Graph, path: str):
        file = open(path, "w")

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

class SvgWriter(WriterInterface):
    @staticmethod
    def write(graph: Graph, path: str):
        file = open(path, "w")
        output = svg.SVG(
            width=graph.boundingBox.x1,
            height=graph.boundingBox.y1,
            elements=[
                svg.Circle(r=1e5, fill="white"),
                svg.Style(text=dedent("""
                    .small { font: 12px Helvetica }
                """))
            ]
        )
        for node in graph.nodes.values():
            output.elements.append(node.shape.toSVG())
            
        for edge in graph.edges:
            output.elements.append(edge.shape.toSVG())

        file.write(str(output))
