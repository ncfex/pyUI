# elements/section.py

from core.element import Element

class Section(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "section"