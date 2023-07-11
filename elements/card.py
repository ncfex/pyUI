# elements/card.py

from core.element import Element

class Card(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "div"
        self.add_class('card')