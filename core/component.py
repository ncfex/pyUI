# core/component.py

from typing import Callable, Optional, Dict, Any
from . import Element
from .renderer import Renderer

class Component(Element):
    def __init__(self, id: Optional[str] = None, connection = None):
        super().__init__(id=id, connection=connection)
        self.build()

    def build(self):
        pass  # override in subclassa