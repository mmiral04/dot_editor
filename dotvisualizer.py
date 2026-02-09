import re

from parser import DotParser
from writer import DotWriter, SvgWriter
from gui import GUI

if __name__ == "__main__":
    #graph = findObjects()
    graph = DotParser.parseFile("afdmanual2.dot")
    GUI(graph, lambda: SvgWriter.write(graph, "output.svg")).start()
