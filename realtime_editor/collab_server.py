from flask_socketio import SocketIO, emit, join_room, leave_room
from realtime_editor.ot_engine import OTEngine

socketio = SocketIO(cors_allowed_origins="*")
documents = {}  # report_id -> {"content": "", "history": []}

@socketio.on('join_edit', namespace='/editor')
def handle_join(data):
    room = data['report_id']
    join_room(room)
    if room not in documents:
        documents[room] = {"content": "", "history": []}
    emit('document_state', documents[room]['content'], to=room)

@socketio.on('edit', namespace='/editor')
def handle_edit(data):
    room = data['report_id']
    operation = data['operation']
    if room not in documents:
        documents[room] = {"content": "", "history": []}
    doc = documents[room]['content']
    new_doc = OTEngine.apply(doc, operation)
    documents[room]['content'] = new_doc
    documents[room]['history'].append(operation)
    emit('update', {'operation': operation, 'source': data.get('user')}, to=room, include_self=False)