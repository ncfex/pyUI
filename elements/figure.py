# elements/figure.py

from core.element import Element

class Figure(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "figure"