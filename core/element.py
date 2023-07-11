# core/element.py

from typing import Optional, List, Dict, Callable, Any
from .renderer import Renderer
import uuid

class Element:    
    _current = None

    def __init__(self, sid: Optional[str] = None, tag: Optional[str] = "div", id: Optional[str] = None, value: Optional[Any] = None, connection = None, **kwargs):
        self.id = id or str(uuid.uuid4())
        self.value = value
        self.tag = tag
        self.children: List['Element'] = []
        self.attrs: Dict[str, str] = kwargs
        self.events: Dict[str, Callable] = {}
        self.classes: List[str] = []
        self.styles: Dict[str, str] = {}
        self.parent = Element._current if Element._current else None
        self.connection = connection or (self.parent.connection if self.parent else None)
        self.sid = sid or (self.parent.sid if self.parent else None)
        self.root = self if self.parent is None else self.parent.root
        self.elements = {} if self.root is self else None

        if self.parent is not None:
            self.parent.children.append(self)
            
        if self.root is not None:
            self.root.elements[self.id] = self
        
    def get_scripts(self):
        return [], ''

    def get_styles(self):
        return []

    def get_all_scripts(self):
        header_scripts, init_scripts = self.get_scripts()
        for child in self.children:
            child_header_scripts, child_init_scripts = child.get_all_scripts()
            header_scripts.extend(child_header_scripts)
            init_scripts += child_init_scripts
        return header_scripts, init_scripts

    def get_all_styles(self):
        styles = self.get_styles()
        for child in self.children:
            styles.extend(child.get_all_styles())
        return styles

    def add_child(self, child: 'Element'):
        child.parent = self
        if child.connection is None:
            child.connection = self.connection
        self.children.append(child)
        return self

    # add_event
    def on(self, event_name: str, handler: Callable):
        self.events[event_name] = handler
        return self

    def handle_event(self, element_id: str, event_name: str, value:None, sid: str):
        if event_name in self.events:
            self.events[event_name](element_id, event_name, value, sid)

    def add_class(self, class_name: str):
        self.classes.append(class_name)
        return self

    def cls(self, class_name: str):
        return self.add_class(class_name)

    def add_style(self, style_name: str, style_value: str):
        self.styles[style_name] = style_value
        return self

    def style(self, style_name: str, style_value: str):
        self.add_style(style_name, style_value)

    def set_attr(self, attr_name: str, attr_value: str):
        self.attrs[attr_name] = attr_value
        return self
    
    def get_client_handler_str(self, event_name):
        return f" on{event_name}='clientEmit(this.id, \"{event_name}\")'"

    def find_element_by_id(self, id: str) -> Optional['Element']:
        return self.root.elements.get(id)

    def Elm(self, id):
        return self.find_element_by_id(id)

    def navigate_to(self, route: str):
        if self.connection and self.connection.router:
            self.connection.router.navigate_to(route, elem_id=self.id, sid=self.sid)

    def render(self):
        return Renderer.render(self)

    def update(self):
        connection = self.connection or (self.parent.connection if self.parent else None)
        
        if connection:
            self.connection.emit("from-server", {"event_name": "update-content", "id": self.id, "value": self.render()}, self.sid)
        

    def __str__(self):
        return self.render()

    def __enter__(self):
        self._prev = Element._current
        Element._current = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Element._current = self._prev