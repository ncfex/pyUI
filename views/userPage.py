# components/userPage.py

from core.element import Element
from elements.button import Button
import random

class UserPage(Element):
    def __init__(self, id="user-page", *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)

        with self:
            Element(id=f"{self.id}-header", value="User Page Header")
            Button(id=f"{self.id}-button", value="TRY EVENTS").add_event("click", self.button_click)
            Button(id=f"{self.id}-button1", value="Go to View Page").add_event("click", self.goTo)
            with Element(id=f"{self.id}-asd", value="DIV"):
                Element(id=f"{self.id}-dsa", value="DIV INSIDE").add_style("color", "red")

    def button_click(self, element_id, event_name, value, sid):
        button = self.find_element_by_id(element_id)
        button.value = "Going to View"
        button.add_style("color", f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})")
        self.Elm(f"{self.id}-header").add_style("background-color", f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})")
        self.Elm(f"{self.id}-dsa").add_style("color", f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})")
        self.Elm(f"{self.id}-dsa").render()
        self.Elm(f"{self.id}-header").render()
        button.render()
        # button.navigate_to("home")
    
    def goTo(self, element_id, event_name, value, sid):
        button = self.find_element_by_id(element_id)
        button.value = "Going to View Page"
        button.add_style("color", f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})")
        button.render()
        button.navigate_to("view")

    def get_scripts(self):
        header_scripts = ["https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.0/jquery.min.js", "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.0/jquery.js"]
        init_script = """
        console.log("This is from userPage")
        """
        return header_scripts, init_script


# from main import run, router

# if __name__ == '__main__':
#     router.add_route("user")
#     run()