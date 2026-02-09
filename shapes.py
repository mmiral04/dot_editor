from abc import ABC, abstractmethod
from tkinter import Canvas
import tkinter.font as tkFont
import svg
from textwrap import dedent

from geometry import Point

class Shape(ABC):
    @abstractmethod
    def render(self, canvas: Canvas):
        raise NotImplementedError
    
    def toSVG(self) -> svg.SVG:
        raise NotImplementedError

class DoubleCircleShape(Shape):
    def __init__(self, pos: Point = None, radius: float = 0, label: str = ""):
        self.pos = pos
        self.radius = radius
        self.label = label

    def clone(self, pos: Point, radius: float, label: str):
        return DoubleCircleShape(pos, radius, label)

    def render(self, canvas):
        doubleCircleWidth = 3
        canvas.create_oval(self.pos.x - self.radius, self.pos.y - self.radius,
                           self.pos.x + self.radius, self.pos.y + self.radius,
                           tags = self.label, fill = "white")
        canvas.create_oval(self.pos.x - self.radius + doubleCircleWidth, 
                           self.pos.y - self.radius + doubleCircleWidth,
                           self.pos.x + self.radius - doubleCircleWidth, 
                           self.pos.y + self.radius - doubleCircleWidth,
                           tags = self.label, fill = "white")
        canvas.create_text(self.pos.x, self.pos.y, text = self.label,
                           font = tkFont.Font(size=7), tags = self.label)
        
    def toSVG(self):
        return svg.SVG(
            elements=[
                svg.Circle(
                    cx=self.pos.x, cy=self.pos.y, r=self.radius,
                    stroke="black", fill="white",
                ),
                svg.Circle(
                    cx=self.pos.x, cy=self.pos.y, r=self.radius - 5,
                    stroke="black", fill="white",
                ),
                svg.Text(
                    x=self.pos.x, y =self.pos.y + 5,
                    text_anchor="middle",
                    text=self.label, stroke="black",
                    stroke_width = 0,
                    class_=["small"]
                )]
            )
    def moveTo(self, pos: Point):
        self.pos = pos

    def __str__(self):
        return "doublecircle"

class CircleShape(Shape):
    def __init__(self, pos: Point = None, radius: float = 0, label: str = ""):
        self.pos = pos
        self.radius = radius
        self.label = label

    def clone(self, pos: Point, radius: float, label: str):
        return CircleShape(pos, radius, label)

    def render(self, canvas):
        canvas.create_oval(self.pos.x - self.radius, self.pos.y - self.radius,
                                self.pos.x + self.radius, self.pos.y + self.radius,
                                tags = self.label, fill = "white")
        canvas.create_text(self.pos.x, self.pos.y, text = self.label,
                                font = tkFont.Font(size=7), tags = self.label)
        
    def toSVG(self) -> svg.SVG:
        return svg.SVG(
            elements=[
                svg.Circle(
                    cx=self.pos.x, cy=self.pos.y, r=self.radius,
                    stroke="black", fill="white",
                ),
                svg.Text(
                    x=self.pos.x, y =self.pos.y + 5,
                    text_anchor="middle",
                    text=self.label, stroke="black",
                    stroke_width = 0,
                    class_=["small"]
                )]
            )
            
    def moveTo(self, pos: Point):
        self.pos = pos

    def __str__(self):
        return "circle"


class Arrow(Shape):
    def __init__(self, origin: Point, dest: Point, label: str):
        self.origin = origin
        self.dest = dest
        self.label = label
        self.id = None

    def moveTo(self, origin: Point, dest: Point):
        self.origin = origin
        self.dest = dest

    def render(self, canvas):
        if self.id != None:
            canvas.delete(self.id)
        self.id = canvas.create_line(self.origin.x, self.origin.y,
                           self.dest.x, self.dest.y,
                           arrow = "last")
        
    def toSVG(self) -> svg.SVG:
        return svg.SVG(
            width=1500,
            height=1500,
            elements=[
                svg.Path(
                    stroke="black",
                    d= f"M {self.origin.x},{self.origin.y}" +
                       f"L {self.dest.x},{self.dest.y}" +
                       f"L {self.dest.x}",
                    stroke_width=1
                )
            ]
        )
    
if __name__ == "__main__":
    file = open("output.svg", "w")
    file.write(str(Arrow(Point(600, 600), Point(800, 900), "label").toSVG()))