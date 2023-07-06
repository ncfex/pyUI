# components/userPage.py

from core.element import Element
from core.component import Component
from elements.button import Button
from components.header import Header

class Error(Component):
    def __init__(self, connection=None, **kwargs):
        super().__init__(id="error-page", **kwargs)
        self.connection = connection
        
        with self:
            Header(id=f"{self.id}-header", text="Error page csty")