# elements/image.py

from core.element import Element
from core.component import Component

class Image(Element):
    def __init__(self, id=None, connection=None, value = None, src =None):
        super().__init__(tag="img", id=id, connection=connection, value=value, src=src)