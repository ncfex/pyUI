# core/element.py

from typing import Optional, List, Dict, Callable, Any
from .renderer import Renderer

class Element:    
    _current = None

    def __init__(self, tag: Optional[str] = "div", id: Optional[str] = None, value: Optional[Any] = None, connection = None):
        self.id = id
        self.value = value
        self.tag = tag
        self.children: List['Element'] = []
        self.attrs: Dict[str, str] = {}
        self.events: Dict[str, Callable[[str, Any], None]] = {}
        self.classes: List[str] = []
        self.styles: Dict[str, str] = {}
        self.parent = None
        self.connection = connection

        if Element._current is not None:
            Element._current.children.append(self)
            self.parent = Element._current
        
    def add_child(self, child: 'Element'):
        child.parent = self
        if child.connection is None:
            child.connection = self.connection
        self.children.append(child)
        return self

    def add_event(self, event: str, callback: Callable[[str, Any], None]):
        self.events[event] = callback
        return self

    def handle_event(self, element_id: str, event_name: str):
        if event_name in self.events:
            self.events[event_name](element_id, event_name)

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
            print(f"Found element {result}")
            if result is not None:
                return result
        return None

    def navigate_to(self, route: str):
        if self.connection and self.connection.router:
            self.connection.router.navigate_to(route)

    def render(self):
        rendered_str = Renderer.render(self)
        
        print(f"Rendering an element {self.id} \n With content of \n {rendered_str}")

        connection = self.connection or (self.parent.connection if self.parent else None)
        
        if connection:
            connection.send(self.id, rendered_str, "update-content")
        
        return rendered_str

    def __enter__(self):
        self._prev = Element._current
        Element._current = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Element._current = self._prev