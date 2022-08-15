import socketio

from apps.cups.internal.variables import user_rooms, user_colours

sessions = {
    # socket_id: user_id
}

# create a Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins=[], async_mode='asgi')


@sio.event
async def connect(sid, environ):
    print('connect ', sid)


@sio.event
async def disconnect(sid):
    print('disconnect')
    await sio.emit('user-event', {"sid": sid, "event": "leave"}, room=user_rooms[sid])

    del user_rooms[sid]
    del user_colours[sid]


@ sio.on('change-colour')
async def change_colour(sid, data):
    print('change_colour', sid, data)

    user_colours[sid] = data['colour']
    await sio.emit('change-colour', {"colour": data['colour'], "sid": sid}, room=user_rooms[sid])

    pass


@ sio.on('join-room')
async def join_room(sid, data):
    print('join_room', sid, data)

    user_rooms[sid] = data['room']
    user_colours[sid] = None
    sio.enter_room(sid, data['room'])
    await sio.emit('user-event', {"sid": sid, "event": "enter"}, room=user_rooms[sid])


@ sio.on('join-room-admin')
async def join_room_admin(sid, data):
    print('join_room_admin', sid, data)

    user_rooms[sid] = data['room']
    sio.enter_room(sid, data['room'])


@ sio.on('leave-room')
async def leave_room(sid, data):
    print('leave_room', sid, data)

    del user_rooms[sid]
    sio.leave_room(sid, data['room'])

# wrap with ASGI application
app = socketio.ASGIApp(sio)
