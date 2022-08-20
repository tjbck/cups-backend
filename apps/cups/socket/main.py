import socketio
from config import REDIS

r = REDIS

# create a Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins=[], async_mode='asgi')


@sio.event
async def connect(sid, environ):
    print('connect ', sid)


@sio.event
async def disconnect(sid):
    print('disconnect')

    room = r.hget(sid, 'room').decode("utf-8")
    await sio.emit('user-event', {"sid": sid, "event": "leave"}, room=room)

    users = r.lrem(f"room:{room}", 0, sid)
    print(users)

    r.hdel(sid, 'room')
    r.hdel(sid, 'colour')
    r.hdel(sid, 'name')


@ sio.on('change-colour')
async def change_colour(sid, data):
    print('change_colour', sid, data)

    room = r.hget(sid, 'room').decode("utf-8")

    r.hmset(sid, {"colour": data['colour']})
    value = r.hget(sid, 'colour')

    await sio.emit('change-colour', {"colour": value, "sid": sid}, room=room)


@ sio.on('join-room')
async def join_room(sid, data):
    print('join_room', sid, data)

    r.hmset(sid, {"room": data['room']})
    room = r.hget(sid, 'room').decode("utf-8")

    users = r.lpush(f"room:{room}", sid)
    print(users, f"room:{room}")

    r.hmset(sid, {"colour": ''})
    colour = r.hget(sid, 'colour')

    sio.enter_room(sid, data['room'])
    await sio.emit('user-event', {"sid": sid, "event": "enter"}, room=room)


@ sio.on('set-username')
async def set_username(sid, data):
    print('set_username', sid, data)

    r.hmset(sid, {"name": data['name']})
    name = r.hget(sid, 'name')

    print(name)


@ sio.on('join-room-admin')
async def join_room_admin(sid, data):
    print('join_room_admin', sid, data)

    r.hmset(sid, {"room": data['room']})
    room = r.hget(sid, 'room').decode("utf-8")

    sio.enter_room(sid, room)


@ sio.on('leave-room')
async def leave_room(sid, data):
    print('leave_room', sid, data)

    room = r.hget(sid, 'room').decode("utf-8")
    r.hdel(sid, 'room')

    sio.leave_room(sid, room)

# wrap with ASGI application
app = socketio.ASGIApp(sio)
