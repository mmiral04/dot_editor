import tkinter as tk
import time


class GUI:
    def __init__(self, graph: Graph, dimensions: Tuple[int, int] = (1500, 1500),
                 title: str = "dot-editor"):
        self.dimensions = dimensions
        self.title = title
        self.graph = graph

        self.root = tk.Tk()
        self.root.geometry(str(self.dimensions[0]) + "x" + str(self.dimensions[1]))
        self.root.title = self.title

        self.canvas = tk.Canvas(self.root, width = self.dimensions[0], height = self.dimensions[1])
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        
        self.nodes = self.graph.nodes
        self.edges = self.graph.edges

    def isCircle(self, x, y):
        for name, (cX, cY, r) in self.objects.items():
            if ((x - cX)**2 + (y - cY)**2 < r**2):
                return name

    def on_drag_start(self, event):
        event.widget.currentObject = self.isCircle(event.x, event.y)
        event.widget.startX = event.x
        event.widget.startY = event.y


    def on_drag_motion(self, event):
        object = event.widget.currentObject
        radius = self.objects[object][2]
        event.widget.delete(object)
        event.widget.create_oval(event.x - radius, event.y - radius,
                                 event.x + radius, event.y + radius, tags = object, fill = "white")
        self.objects[object] = (event.x, event.y, radius)

    def start(self):
        for node in self.nodes.values():
            node.render(self.canvas)
        self.root.mainloop()

