# main.py

from flask import Flask
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

# ROUTER
router = Router(connection)
router.add_route("home", HomePage)
router.add_route("user", UserPage)
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

    header_items = [
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>Document</title>',
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.2.0/socket.io.js"></script>',
    ]
    header = "\n".join(header_items)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        {header}
    </head>
    <body>
        {component.render()}
        <script>
            const socket = io();
            socket.on("connect", function() {{
                console.log("Connected to server");
            }});
            socket.on("disconnect", function() {{
                console.log("Disconnected from server");
            }});
            socket.on('from_server', function(data) {{
                console.log('Received message from server:', data);
                let element = document.getElementById(data.id);
                if (element) {{
                    element.innerText = data.value;
                }}
            }});
            socket.on('update-content', function(data) {{
                console.log('Received update-content message from server:', data);
                let element = document.getElementById(data.id);
                if (element) {{
                    element.outerHTML = data.value;
                }}
            }});
            socket.on('navigate_to', function(data) {{
                console.log('Received navigate message from server:', data);
                window.location = "/" + data.value;
            }});
            function clientEmit(id, event_name) {{
                console.log(id, event_name)
                socket.emit('from_client', {{id: id, event_name: event_name}});
            }}
        </script>
    </body>
    </html>
    """
@socketio.on('from_client')
def handle_message(data):
    print('Received message:', data)
    connection.receive_from_client(data)

if __name__ == '__main__':
    socketio.run(app)
