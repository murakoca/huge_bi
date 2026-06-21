from flask_socketio import SocketIO, emit, join_room, leave_room

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('join_report', namespace='/collab')
def handle_join(data):
    room = data['report_id']
    join_room(room)
    emit('user_joined', {'user': data['user']}, to=room)

@socketio.on('cursor_move', namespace='/collab')
def handle_cursor(data):
    room = data['report_id']
    emit('cursor_update', {'user': data['user'], 'position': data['position']}, to=room, include_self=False)

@socketio.on('comment_added', namespace='/collab')
def handle_comment(data):
    room = data['report_id']
    emit('new_comment', {'user': data['user'], 'comment': data['comment']}, to=room)