# elements/canvas.py

from core.element import Element

class Canvas(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "canvas"

    def width(self, value):
        self.attrs["width"] = value
        return self
    
    def height(self, value):
        self.attrs["height"] = value
        return self

    def get_scripts(self):
        header_scripts = []
        init_scripts = """
        window.event_handlers["init-canvas"] = function(id, value, event_name){     
            console.log(id, value, event_name, "init-canvas")       
            canvas = document.getElementById(id);
            elements[id] = {canvas: canvas, ctx: canvas.getContext('2d')};            
        }
        window.event_handlers["canvas"] = function(id, value, event_name){        
            console.log(id, value, event_name, "canvas")
            if (value.action == "fillRect"){
                elements[id].ctx.fillStyle = value.params.color;
                elements[id].ctx.fillRect(value.params.x, value.params.y, value.params.width, value.params.height);
            }
            if (value.action == "fillCircle"){
                elements[id].ctx.beginPath();
                elements[id].ctx.arc(value.params.x, value.params.y, value.params.radius, 0, 2 * Math.PI);
                elements[id].ctx.fillStyle = value.params.color;
                elements[id].ctx.fill();
            }
        }
        """
        return header_scripts, init_scripts
    
    def fill_rect(self, x, y, width, height,color):
        self.connection.emit("from-server",
                            {"event_name": "canvas", "id": self.id, "value":
                                {"action": "fillRect","params":
                                    {"x": x, "y": y, "width": width, "height": height, "color": color}
                                }
                            }, self.sid)
        return self
    
    def fill_circle(self, x, y, radius,color):
        self.connection.emit("from-server",
                            {"event_name": "canvas", "id": self.id, "value":
                                {"action": "fillCircle",
                                    "params": {"x": x, "y": y, "radius": radius, "color":color}
                                }
                            }, self.sid)
        return self

    def get_client_handler_str(self, event_name):
        if event_name in ["mousedown", "mouseup", "mousemove"]:
            return f" on{event_name}='clientEmit(this.id,\"{event_name}\",{{x: event.offsetX, y: event.offsetY}})'"
        else:
            return super().get_client_handler_str(event_name)