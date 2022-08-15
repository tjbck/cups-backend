
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.cups.routers import rooms
from apps.cups.socket.main import app as socket_app

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(rooms.router)
app.mount("/ws", socket_app, name="socket")
