from typing import Optional, Dict, Callable, Any
from flask_socketio import SocketIO
from .component import Component
import uuid

class Connection:
    def __init__(self, router=None):
        self.clients: Dict[str, Dict[str, 'Component']] = {}
        self.socket: Optional[SocketIO] = None
        self.router = router

    def register_component(self, component: 'Component', sid: str):
        component.id = component.id or str(uuid.uuid4())
        if sid not in self.clients:
            self.clients[sid] = {}
        self.clients[sid][component.id] = component
        print(f'component registered as  {component} to user {sid}\nUsers components: {self.clients[sid]}')
    
    def remove_client(self, sid: str):
        if sid in self.clients:
            del self.clients[sid]
    
    def emit(self, sid: str, event: str, payload: Any):
        if self.socket is not None:
            self.socket.emit(event, payload, room=sid)

    def receive(self, data: Dict[str, str], sid: str):
        element_id = data["id"]
        event_name = data["event_name"]

        if self.clients.get(sid) is None:
            return None

        for component in self.clients[sid].values():
            element = component.find_element_by_id(element_id)
            if element is not None:
                print(f"Found element {element_id} -> {element} => FROM CONNECTION.RECEIVE")
                element.handle_event(element_id, event_name, sid)
                break