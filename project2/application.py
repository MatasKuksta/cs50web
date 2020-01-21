import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__)
os.getenv("SECRET_KEY")
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

strdData = {  'stored_data': {
            'channels': ['default'],
            'currentChannel': 'default',
            'messages': {'default': []},
            'username': ''
            }}

@socketio.on('sendmsg')
def handle_my_custom_event(messageData, methods=['GET', 'POST']):
    print('recieved my event: '+ str(messageData))
    global strdData
    strdData = messageData
    socketio.emit('my response', messageData);


@socketio.on('connect')
def handle_my_event(methods=['GET', 'POST']):
    emit('load', strdData)


if __name__ == '__main__':
    socketio.run(app, debug=True)
