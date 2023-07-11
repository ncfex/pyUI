# elements/image.py

from core.element import Element

class Image(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "img"