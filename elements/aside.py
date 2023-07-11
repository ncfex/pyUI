# elements/aside.py

from core.element import Element

class Aside(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "aside"