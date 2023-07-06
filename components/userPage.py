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
            Button(id=f"{self.id}-button", value="Go to Home", connection=self.connection).add_event("click", self.button_click)

    def button_click(self, element_id, event_name, sid):
        button = self.find_element_by_id(element_id)
        print(button)
        # button.value = "Going to Home"
        # button.navigate_to("home")