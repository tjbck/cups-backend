
from typing import Union, List
from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status

from apps.cups.internal.constants import ERROR_MESSAGES
from config import REDIS
r = REDIS


router = APIRouter()


class MarkQuetionForm(BaseModel):
    content: str


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


@router.get("/rooms/{room_id}/questions", tags=["rooms"])
async def get_questions_in_room(room_id: str):
    questions_key = f'questions:{room_id}'
    questions_length = r.llen(questions_key)
    questions = r.lrange(questions_key, 0, questions_length)

    return questions


@router.post("/rooms/{room_id}/questions/mark", tags=["rooms"])
async def mark_quetion_as_answered(room_id: str, form_data: MarkQuetionForm):

    removed_count = r.lrem(f"questions:{room_id}", 0, form_data.content)

    return True if removed_count else False
