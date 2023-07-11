from typing import Optional, Dict, Callable, Any
from flask_socketio import SocketIO
from .element import Element
import uuid

class Connection:
    def __init__(self, router=None):
        self.clients: Dict[str, Dict[str, 'Element']] = {}
        self.socket: Optional[SocketIO] = None
        self.router = router

    def register_view(self, view: 'Element', sid: str):
        view.sid = sid  # store sid in view
        view.id = view.id or str(uuid.uuid4())
        if sid not in self.clients:
            self.clients[sid] = {}
        self.clients[sid][view.id] = view
        print(f'view registered as  {view} to user {sid}\nUsers views: {self.clients[sid]}')

    def remove_client(self, sid: str):
        if sid in self.clients:
            del self.clients[sid]
    
    def emit(self, event: str, payload: Any, sid: str):
        if self.socket is not None:
            print(f"Checking for {sid} in rooms")
            self.socket.emit(event, payload, room=sid)
            
    def receive(self, data: Dict[str, str], sid: str):
        element_id = data["id"]
        event_name = data["event_name"]
        value = data.get("value", None)
        print(f"Received event {event_name} from {element_id} with value {value} => FROM CONNECTION.RECEIVE")

        if self.clients.get(sid) is None:
            return None

        for view in self.clients[sid].values():
            element = view.find_element_by_id(element_id)
            if element is not None:
                print(f"Found element {element_id} -> {element} => FROM CONNECTION.RECEIVE")
                element.handle_event(element.id, event_name, value, element.sid)
                break