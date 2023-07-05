# core/connection.py

from typing import Optional, Dict, Callable, Any
from flask_socketio import SocketIO
from .component import Component
import uuid

class Connection:
    def __init__(self, router=None):
        self.components: Dict[str, 'Component'] = {}
        self.socket: Optional[SocketIO] = None
        self.router = router

    def register_component(self, component: Component):
        component.id = component.id or str(uuid.uuid4())
        self.components[component.id] = component
        print(f'component registered as', component)

    def send(self, id: str, value: str, event_name: str = "from_server"):
        if self.socket is not None:
            self.socket.emit(event_name, {"id": id, "value": value})

    def receive_from_client(self, data: Dict[str, str]):
        element_id = data["id"]
        event_name = data["event_name"]

        print(f"Received {event_name} from {element_id}")

        for component in self.components.values():
            element = component.find_element_by_id(element_id)
            if element is not None:
                element.handle_event(element_id, event_name)
                break