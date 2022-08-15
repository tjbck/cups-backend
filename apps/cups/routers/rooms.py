
from typing import Union, List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status


from apps.cups.internal.constants import ERROR_MESSAGES
from apps.cups.internal.variables import user_rooms, user_colours


router = APIRouter()


@router.get("/rooms/user/{socket_id}", tags=["rooms"])
async def get_user_room(socket_id: str):

    if(socket_id in user_rooms):
        return user_rooms[socket_id]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES['DEFAULT'])


@router.get("/rooms/{room_id}", tags=["rooms"])
async def get_room_info(room_id: str):
    user_list = [sid for sid
                 in user_rooms if user_rooms[sid] == room_id]

    colour_list = [{"sid": sid, "colour": user_colours[sid]}
                   for sid in user_colours if sid in user_list]

    return colour_list
