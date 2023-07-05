# elements/col.py

from core.element import Element

class Col(Element):
    def __init__(self, id=None, connection=None, value = None):
        super().__init__(tag="div", id=id, connection=connection, value=value)