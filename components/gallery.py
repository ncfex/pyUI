# components/userPage.py

from core.element import Element
from core.component import Component
from elements.button import Button
from elements.image import Image
from components.header import Header

class Gallery(Element):
    def __init__(self, connection=None, **kwargs):
        super().__init__(id="gallery-page", **kwargs)
        self.connection = connection
        
        with self:
            Image(id=f"{self.id}-image-1", src="https://www.ait.com.tr/wp-content/themes/aittema/images/logo.svg")
            Image(id=f"{self.id}-image-1", src="https://www.ait.com.tr/wp-content/themes/aittema/images/logo.svg")
            Image(id=f"{self.id}-image-1", src="https://www.ait.com.tr/wp-content/themes/aittema/images/logo.svg")
            Image(id=f"{self.id}-image-1", src="https://www.ait.com.tr/wp-content/themes/aittema/images/logo.svg")
            with Element() as div:
                Image(id=f"{self.id}-image-1", src="https://www.ait.com.tr/wp-content/themes/aittema/images/logo.svg")
                Image(id=f"{self.id}-image-1", src="https://www.ait.com.tr/wp-content/themes/aittema/images/logo.svg")