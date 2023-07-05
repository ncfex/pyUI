# core/renderer.py
class Renderer:
    @staticmethod
    def render(element):
        attrs_str = " ".join([f'{k}="{v}"' for k, v in element.attrs.items()])
        classes_str = " ".join(element.classes)
        styles_str = "; ".join([f'{k}: {v}' for k, v in element.styles.items()])
        children_str = "\n".join([Renderer.render(child) for child in element.children])

        print(f"children_str of {element.id} \n => {children_str}")

        events_str = ""
        for event_name, action in element.events.items():
            event_handler_str = element.get_client_handler_str(event_name)
            events_str += f" '{event_handler_str}'"

        return f'<{element.tag} id="{element.id}" class="{classes_str}" style="{styles_str}" {attrs_str}{events_str}>{element.value if element.value is not None else ""}\n{children_str}\n</{element.tag}>'