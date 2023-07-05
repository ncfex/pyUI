# components/header.py

from core.element import Element
from elements.h1 import H1

class Header(Element):
    def __init__(self, connection, text):
        super().__init__(tag="header", id="header", connection=connection)
        self.header_text = text
        self.build()

    def build(self):
        self.header_element = H1(id=f"{self.id}-h1", value=self.header_text)
        self.add_child(self.header_element)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self
