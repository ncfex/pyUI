# elements/article.py

from core.element import Element

class Article(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "article"