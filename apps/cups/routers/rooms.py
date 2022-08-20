
from typing import Union, List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status

from apps.cups.internal.constants import ERROR_MESSAGES
from config import REDIS
r = REDIS


router = APIRouter()


@router.get("/rooms/user/{socket_id}", tags=["rooms"])
async def get_user_room(socket_id: str):
    room = r.hget(socket_id, 'room')
    if room:
        return room
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES['DEFAULT'])


@router.get("/rooms/{room_id}", tags=["rooms"])
async def get_room_info(room_id: str):
    room_name = f'room:{room_id}'

    users_length = r.llen(room_name)
    users = r.lrange(room_name, 0, users_length)

    return [r.hgetall(user.decode('utf-8')) for user in users]
