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
            'channels': [],
            'messages': {'default': []}
            }}

@socketio.on('sendmsg')
def handle_my_custom_event(messageData, methods=['GET', 'POST']):
    print('recieved my event: '+ str(messageData))
    global strdData
    strdData = messageData
    socketio.emit('my response', messageData);

print('Strd data: '+ str(strdData))

@socketio.on('connect')
def handle_my_event(methods=['GET', 'POST']):
    emit('load', strdData)
    # socketio.emit('my respon', json)


# @socketio.on('join')
# def on_join(data):
#     username = data['username']
#     room = data['room']
#     join_room(room)
#     send(username + ' has entered the room.', room=room)
#
# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send(username + ' has left the room.', room=room)


# @socketio.on('send')
# def on_send(json)


if __name__ == '__main__':
    socketio.run(app, debug=True)
