import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.cups.main import app as cups_v1_app
from config import ENV

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_status():
    return {"status": True, "python": sys.version, "env": ENV}


app.mount("/v1", cups_v1_app)
