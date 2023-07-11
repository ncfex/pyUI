# elements/figure.py

from core.element import Element

class Footer(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "footer"