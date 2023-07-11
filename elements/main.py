# elements/main.py

from core.element import Element

class Main(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "main"