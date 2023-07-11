# elements/header.py

from core.element import Element

class Header(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "header"