from flask import Flask, render_template, request, make_response, session
from flask_socketio import SocketIO, join_room
from core.connection import Connection
from core.router import Router
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")  # Set the path option
socketio.init_app(app)  # Initialize Flask-SocketIO

connection = Connection()
connection.socket = socketio

from components.homePage import HomePage
from components.userPage import UserPage
from components.fileUpload import FileUploadComponent
from components.gallery import Gallery
from components.error import Error

# ROUTER
router = Router(connection, {})
router.add_route("home", HomePage)
router.add_route("user", UserPage)
router.add_route("dropzone", FileUploadComponent)
router.add_route("gallery", Gallery)
router.add_route("error", Error)
connection.router = router
# ROUTER

@socketio.on('from_client')
def handle_message(data):
    connection.receive(data, request.sid)

@socketio.on('connect')
def handle_connect():
    if 'client_id' not in session:
        # This is a new client, so generate a new ID for them
        session['client_id'] = str(uuid.uuid4())
    sid = session['client_id']
    print(f"Connected a client with sid of {sid}")
    join_room(sid)

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Clint disconnected with sid of {request.sid}")
    connection.remove_client(request.sid)

@app.route('/')
@app.route('/<path:route>')
# def index(path):
#     path_parts = path.split("/")
#     if "favicon.ico" in path_parts:
#         return ""

#     print(f"{path} looking for route")

#     component = router.get_component(path) if path else router.get_component('home')
#     if not component:
#         component = router.get_component('error')

#     sid = session.get('client_id')
#     if sid:
#         connection.register_component(component, sid)
#     else:
#         component = router.get_component('error')

#     component_scripts, component_init_script = component.get_scripts()
#     styles = component.get_styles()

#     scripts = [
#         "https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.2.0/socket.io.js",
#         *component_scripts,
#     ]

#     return render_template("index.html", scripts=scripts, component=component.render(),
#                        component_init_script=component_init_script, styles=styles)
def index(route=None):
    if route == "favicon.ico":
        return ""

    component = router.get_component(route) if route else router.get_component('home')
    if not component:
        component = router.get_component('error')

    sid = session.get('client_id')
    if sid:
        connection.register_component(component, sid)
    else:
        component = router.get_component('error')

    component_scripts, component_init_script = component.get_scripts()
    styles = component.get_styles()

    scripts = [
        "https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.2.0/socket.io.js",
        *component_scripts,
    ]

    return render_template("index.html", scripts=scripts, component=component.render(),
                       component_init_script=component_init_script, styles=styles)

if __name__ == '__main__':
    port=5000
    app.run(host="0.0.0.0",port=port)
