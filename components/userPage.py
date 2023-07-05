# components/userPage.py

from core.element import Element
from core.component import Component
from elements.button import Button
from components.header import Header

class UserPage(Component):
    def __init__(self, connection=None, **kwargs):
        super().__init__(id="user-page", **kwargs)
        self.connection = connection
        
        with self:
            Header(id=f"{self.id}-header", text="Welcome to UserPage")

            with Element(tag="div", id=f"{self.id}-main"):
                Element(id=f"{self.id}-main-p", tag='p', value="This is the main content of the user page.")

            Element(tag="div", id=f"{self.id}-footer", value="This is the footer of the user page.")

            Button(id=f"{self.id}-button", value="Go to Home", connection=self.connection).add_event("click", self.button_click)

    def button_click(self, element_id, event_name):
        button = self.find_element_by_id(f"{self.id}-button")
        button.value = "Going to Home"
        button.navigate_to("home")