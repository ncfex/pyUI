# elements/button.py

from core.element import Element

class Button(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "button"