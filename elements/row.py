# elements/row.py

from typing import Optional, List, Dict, Callable, Any
from .element import Element

class Row(Element):
    def __init__(self, id: Optional[str] = None, connection = None):
        super().__init__(tag='div', id=id, connection=connection)