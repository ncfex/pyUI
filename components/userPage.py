# components/userPage.py

from core.element import Element
from elements.button import Button
import random

class UserPage(Element):
    def __init__(self, sid: str, connection=None, **kwargs):
        super().__init__(sid, id="user-page", connection=connection, **kwargs)
        
        with self:
            print(sid)
            Element(sid, id=f"{self.id}-header", value="User Page Header", connection=self.connection)
            Button(sid, id=f"{self.id}-button", value="Go to Home", connection=self.connection).add_event("click", self.button_click)
            with Element(sid, id=f"{self.id}-asd", value="DIV", connection=self.connection) as div:
                Element(sid, id=f"{self.id}-dsa", value="DIV INSIDE", connection=self.connection).add_style("color", "red")
            # Add more nested elements as required

    def button_click(self, element_id, event_name, sid):
        button = self.find_element_by_id(element_id)
        button.value = "Going to Home"
        button.add_style("color", f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})")
        print(button.render())
        # button.navigate_to("home")
