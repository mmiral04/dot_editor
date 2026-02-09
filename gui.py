import tkinter as tk
import time
from typing import Tuple

from geometry import Point
from graph import Graph

class GUI:
    def __init__(self, graph: Graph, saveCallback, dimensions: Tuple[int, int] = (1500, 1500),
                 title: str = "dot-editor"):
        self.dimensions = dimensions
        self.title = title

        self.root = tk.Tk()
        self.root.geometry(str(self.dimensions[0]) + "x" + str(self.dimensions[1]))
        self.root.title = self.title

        self.canvas = tk.Canvas(self.root, width = self.dimensions[0], height = self.dimensions[1])
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_stop)

        saveButton = tk.Button(self.root, text = "save", command=lambda: saveCallback())
        self.canvas.create_window(40, 20, window=saveButton)
        
        self.nodes = graph.nodes
        self.edges = graph.edges

    def isCircle(self, x, y):
        for name, node in self.nodes.items():
            if ((x - node.pos.x)**2 + (y - node.pos.y)**2 < node.width**2):
                return name

    def on_drag_start(self, event):
        event.widget.currentObject = self.isCircle(event.x, event.y)

    def on_drag_motion(self, event):
        if event.widget.currentObject == None:
            return
        object = self.nodes[event.widget.currentObject]
        event.widget.delete(event.widget.currentObject)
        object.moveTo(Point(event.x, event.y))
        object.render(self.canvas)

    def on_drag_stop(self, event):
        event.widget.currentObject = None

    def start(self):
        for node in self.nodes.values():
            node.render(self.canvas)
        for edge in self.edges:
            edge.render(self.canvas)
        self.root.mainloop()

