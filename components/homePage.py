# components/homePage.py

from core.element import Element
from elements.button import Button
from components.header import Header

class HomePage(Element):
    def __init__(self, connection=None, **kwargs):
        super().__init__(tag='div', id="home-page", **kwargs)
        self.connection = connection

        with self:
            Header(text="Welcome to HomePage")