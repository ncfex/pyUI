# components/userPage.py

from core.element import Element
from core.component import Component
from elements.button import Button
from components.header import Header

class FileUploadComponent(Element):
    def __init__(self, connection=None, **kwargs):
        super().__init__(id="dropzone-page", **kwargs)
        self.connection = connection
        
        with self:
            with Element(id=f"{self.id}-div").add_style("height", "100%") as div:
                Element(id=f"dropzone").add_style("height", "100px").add_style("width", "200px")

    def get_styles(self):
        styles = ["https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.3/dropzone.min.css"]
        return styles

    def get_scripts(self):
        scripts = ["https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.2/dropzone.js"]
        init_script = """
        Dropzone.autoDiscover = false;

        var myDropzone = new Dropzone("#dropzone", {
          url: "/upload", // Specify the URL for file uploads
        });
        """
        return scripts, init_script