# components/canvasPage.py

from core.element import Element
from elements.button import Button
from elements.canvas import Canvas

import random

class CanvasPage(Element):
    def __init__(self, id="user-page", *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)

        with self:
            canvas = Canvas(id=f"{self.id}-canvas").width(500).height(500).add_style("background", "white")
            canvas.on("mousedown", self.on_mouse_down)
            canvas.on("mouseup", self.on_mouse_up)
            canvas.on("mousemove", self.on_mouse_move)
            Button(id=f"{self.id}-init-cnv-btn").on("click", self.init_canvas).value = "INIT CANVAS"

    mouse_down = False
    selected_color = "black"
    colors = ["red", "green", "blue", "yellow", "black", "white"]
    radius = 10

    def init_canvas(self, element_id, event_name, value, sid):
        self.connection.emit("from-server", {"event_name": "init-canvas", "id": f"{self.id}-canvas", "value": "1" }, self.sid)

    def on_mouse_down(self, element_id, event_name, value, sid):
        global mouse_down
        mouse_down = True
        print("on_mouse_down", element_id, value)
        self.Elm(element_id).fill_rect(value["x"], value["y"], 10, 10, self.selected_color)

    def on_mouse_up(self, element_id, event_name, value, sid):
        global mouse_down
        mouse_down = False
        print("on_mouse_up", element_id, value)

    def on_mouse_move(self, element_id, event_name, value, sid):
        global mouse_down
        if mouse_down:
            print("on_mouse_move", element_id, value)
            self.Elm(element_id).fill_circle(value["x"], value["y"], self.radius, self.selected_color)