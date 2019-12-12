import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__)
app.config["SECRET_KEY"] = 'vnkdjnfjknfl1232#'
# os.getenv("SECRET_KEY")
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('recieved my event: '+ str(json))
    socketio.emit('my response', json)

if __name__ == '__main__':
    socketio.run(app, debug=True)
