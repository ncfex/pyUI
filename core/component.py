# core/component.py

from typing import Callable, Optional, Dict, Any
from . import Element
from .renderer import Renderer

class Component(Element):
    def __init__(self, id: Optional[str] = None, connection = None):
        super().__init__(id=id, connection=connection)
        self.build()

    def build(self):
        pass  # override in subclass
    
    def render(self):
        rendered_str = Renderer.render(self)
        
        print(f"Rendering a component {self.id}")

        connection = self.connection or (self.parent.connection if self.parent else None)
        if connection:
            connection.send(self.id, rendered_str, "update-content")
        
        return rendered_str

    def handle_event(self, value: str, event_name: str):
        if event_name in self.events:
            self.events[event_name](self, value)
    
    def add_event(self, event: str, callback: Callable[[str, Any], None]):
        self.events[event] = callback
        return self

    def find_element(self, id: str) -> Optional[Element]:
        if self.id == id:
            return self
        for child in self.children:
            found = child.find_element_by_id(id)
            if found is not None:
                return found
        return None

    def navigate_to(self, route: str):
        if self.connection and self.connection.router:
            self.connection.router.navigate_to(route)

## TESTING CUSTOM COMPONENTS
# core/component.py
from elements.button import Button
from components.header import Header

class HomePage(Component):
    def __init__(self, connection):
        super().__init__(id="home-page", connection=connection)

    def build(self):
        self.header = Header(connection=self.connection, text="Welcome to HomePage")
        self.main = Element(tag="div", id=f"{self.id}-main", value="This is the main content of the homepage.")
        self.footer = Element(tag="div", id=f"{self.id}-footer", value="This is the footer of the homepage.")

        with self:
            self.add_child(self.header)
            self.add_child(self.main)
            self.add_child(self.footer)

class UserPage(Component):
    def __init__(self, connection):
        super().__init__(id="user-page", connection=connection)

    def build(self):
        self.header = Header(connection=self.connection, text="Welcome to UserPage")
        self.main = Element(tag="div", id=f"{self.id}-main", value="This is the main content of the user page.")
        self.footer = Element(tag="div", id=f"{self.id}-footer", value="This is the footer of the user page.")
        self.button = Button(id=f"{self.id}-button", value="Go to Home", connection=self.connection).add_event("click", self.button_click)
        
        with self:
            self.add_child(self.header)
            self.add_child(self.main)
            self.add_child(self.footer)
            self.add_child(self.button)

    def button_click(self, element_id, event):
        element = self.find_element(element_id)
        if element:
            element.value = "This is the updated main content of the homepage."
            # element.render()
            self.navigate_to("home")
        else:
            print("home page not found")