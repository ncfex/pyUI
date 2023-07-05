# components/header.py

from core.element import Element

class Header(Element):
    def __init__(self, text: str, **kwargs):
        super().__init__(tag='header', value=text, **kwargs)