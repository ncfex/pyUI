# elements/h1.py

from core.element import Element

class H1(Element):
    def __init__(self, id: str = None, value: str = None, connection = None):
        super().__init__(tag="h1", id=id, value=value, connection=connection)
        self.build()

    def build(self):
        pass
