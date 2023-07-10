from flask import Flask, render_template, request, make_response, session
from flask_socketio import SocketIO, join_room, rooms
from flask_session import Session
from core.connection import Connection
from core.router import Router
import uuid


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app, manage_session=False, cors_allowed_origins="*")
socketio.init_app(app)  # Initialize Flask-SocketIO
Session(app)

connection = Connection()
connection.socket = socketio

from views.userPage import UserPage
from views.imageViewerPage import ImageViewerPage

# ROUTER
router = Router(connection, {})
router.add_route("user", UserPage)
router.add_route("view", ImageViewerPage)
connection.router = router
# ROUTER

@socketio.on('from-client')
def handle_message(data):
    print(f"Received from {session['client_id']} => {data}")
    connection.receive(data, session['client_id'])

@socketio.on('connect')
def handle_connect():
    if 'client_id' not in session:
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
def index(route=None):
    if route == "favicon.ico":
        return ""

    sid = session.get('client_id', str(uuid.uuid4()))  # default to new UUID if client_id not in session
    session['client_id'] = sid  # set the session ID

    view = router.get_view(route, sid) if route else router.get_view('home', sid)
    if not view:
        return "Route not found"
    connection.register_view(view, sid)

    view_scripts, view_init_script = view.get_all_scripts()
    styles = view.get_all_styles()

    scripts = [
        "https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.2.0/socket.io.js",
        *view_scripts,
    ]

    return render_template("index.html", scripts=scripts, view=view.render(),
                       view_init_script=[view_init_script], styles=styles)

if __name__ == '__main__':
    port=5000
    app.run(host="0.0.0.0",port=port)