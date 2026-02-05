from abc import ABC, abstractmethod
from tkinter import Canvas
import tkinter.font as tkFont

from geometry import Point

class Shape(ABC):
    @abstractmethod
    def render(self, canvas: Canvas):
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
        
    def moveTo(self, pos: Point):
        self.pos = pos

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
        
    def moveTo(self, pos: Point):
        self.pos = pos


class Arrow(Shape):
    def __init__(self, origin: Point, dest: Point, label: str):
        self.origin = origin
        self.dest = dest
        self.label = label

    def render(self, canvas):
        canvas.create_line(self.origin.x, self.origin.y,
                           self.dest.x, self.dest.y,
                           arrow = "last")