# main.py

from flask import Flask, render_template
from flask_socketio import SocketIO
from core.connection import Connection
from core.router import Router

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
socketio.init_app(app)  # Initialize Flask-SocketIO

connection = Connection()
connection.socket = socketio

from components.homePage import HomePage
from components.userPage import UserPage
from components.fileUpload import FileUploadComponent
from components.gallery import Gallery

# ROUTER
router = Router(connection)
router.add_route("home", HomePage)
router.add_route("user", UserPage)
router.add_route("dropzone", FileUploadComponent)
router.add_route("gallery", Gallery)
connection.router = router
# ROUTER

@app.route('/')
@app.route('/<path:route>')
def index(route=None):
    if route == "favicon.ico":
        return ""

    component = router.get_component(route) if route else router.get_component('home')
    if not component:
        component = router.get_component('error')

    connection.register_component(component)

    component_scripts, component_init_script = component.get_scripts()
    styles = component.get_styles()

    scripts = [
        "https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.2.0/socket.io.js",
        *component_scripts,
    ]

    return render_template("index.html", scripts=scripts, component=component.render(),
                       component_init_script=component_init_script, styles=styles)
    
@socketio.on('from_client')
def handle_message(data):
    print('Received message:', data)
    connection.receive_from_client(data)

if __name__ == '__main__':
    socketio.run(app)