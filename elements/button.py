# elements/button.py

from core.element import Element

class Button(Element):
    def __init__(self, id=None, connection=None, value = "Button"):
        super().__init__(tag="button", id=id, connection=connection, value=value)
        self.build()

    def build(self):
        pass
