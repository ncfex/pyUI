# elements/button.py

from core.element import Element

class Button(Element):
    def __init__(self, sid: str, connection= None, *args, **kwargs):
        super().__init__(sid, *args, **kwargs)
        self.connection = connection
        self.tag = "button"