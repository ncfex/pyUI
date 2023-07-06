# core/element.py

from typing import Optional, List, Dict, Callable, Any
from .renderer import Renderer
import uuid

class Element:    
    _current = None

    def __init__(self, sid:str, tag: Optional[str] = "div", id: Optional[str] = None, value: Optional[Any] = None, connection = None, **kwargs):
        self.id = id or str(uuid.uuid4())
        self.value = value
        self.tag = tag
        self.children: List['Element'] = []
        self.attrs: Dict[str, str] = kwargs
        self.events: Dict[str, Callable[[str, Any], None]] = {}
        self.classes: List[str] = []
        self.styles: Dict[str, str] = {}
        self.parent = None
        self.connection = connection
        self.sid = sid

        if Element._current is not None:
            Element._current.children.append(self)
            self.parent = Element._current
        
    def get_scripts(self):
        return [], ''

    def get_styles(self):
        return []

    def add_child(self, child: 'Element'):
        child.parent = self
        if child.connection is None:
            child.connection = self.connection
        self.children.append(child)
        return self

    def add_event(self, event: str, callback: Callable[[str, Any], None]):
        self.events[event] = callback
        return self

    def handle_event(self, element_id: str, event_name: str, sid: str):
        if event_name in self.events:
            self.events[event_name](element_id, event_name, sid)

    def add_class(self, class_name: str):
        self.classes.append(class_name)
        return self

    def cls(self, class_name: str):
        return self.add_class(class_name)

    def add_style(self, style_name: str, style_value: str):
        self.styles[style_name] = style_value
        return self

    def set_attr(self, attr_name: str, attr_value: str):
        self.attrs[attr_name] = attr_value
        return self
    
    def get_client_handler_str(self, event_name):
        return f" on{event_name}='clientEmit(this.id, \"{event_name}\")'"

    def find_element_by_id(self, id: str) -> Optional['Element']:
        if self.id == id:
            return self
        for child in self.children:
            if child.id == id:
                return child
            result = child.find_element_by_id(id)
            if result is not None:
                print(f"Found element {result}")
                return result
        return None

    def Elm(self, id):
      return self.find_element_by_id(id)

    def navigate_to(self, route: str):
        if self.connection and self.connection.router:
            self.connection.router.navigate_to(route)

    def render(self):
        rendered_str = Renderer.render(self)

        connection = self.connection or (self.parent.connection if self.parent else None)
        
        if connection:
            connection.emit("update-content", { "id": self.id, "value": rendered_str }, self.sid)
        return rendered_str

    def __enter__(self):
        self._prev = Element._current
        Element._current = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Element._current = self._prev