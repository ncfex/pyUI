# elements/form.py

from core.element import Element

class Form(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "form"