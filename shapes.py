from abc import ABC
import tkinter.font as tkFont

class Shape(ABC):
    pass

class DoubleCircleShape(Shape):
    def render(self, canvas: Canvas, pos: Tuple[float, float], radius: float, label: str):
        canvas.create_oval(pos[0] - radius, pos[1] - radius,
                           pos[0] + radius, pos[1] + radius,
                           tags = label, fill = "white")
        canvas.create_text(pos[0], pos[1], text = label, font = tkFont.Font(size=7))

class CircleShape(Shape):
    def render(self, canvas: Canvas, pos: Tuple[float, float], radius: float, label: str):
        canvas.create_oval(pos[0] - radius, pos[1] - radius,
                           pos[0] + radius, pos[1] + radius,
                           tags = label, fill = "white")
        canvas.create_text(pos[0], pos[1], text = label, font = tkFont.Font(size=7))


