# components/homePage.py

from core.element import Element
from elements.button import Button
from components.header import Header

class HomePage(Element):
    def __init__(self, connection=None, **kwargs):
        super().__init__(tag='div', id="home-page", **kwargs)
        self.connection = connection

        with self:
            Header(text="Welcome to HomePage")
            
            with Element(tag="div", id=f"{self.id}-main"):
                Element(tag='p', value="This is the main content of the homepage.")
                Button(id=f"{self.id}-button", value="Go to User", connection=self.connection).add_event("click", self.button_click)

            Element(tag="div", id=f"{self.id}-footer", value="This is the footer of the homepage.")
    
    def button_click(self, element_id, event_name):
        button = self.find_element_by_id(f"{self.id}-button")
        button.value = "Going to User"
        button.render()
        button.navigate_to("user")