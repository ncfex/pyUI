# elements/nav.py

from core.element import Element

class Nav(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "nav"