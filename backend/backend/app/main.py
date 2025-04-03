from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, players, rooms
from .database import Base, engine
from .ws import ws_api

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(players.router)
app.include_router(rooms.router)
app.include_router(ws_api.router)

@app.get("/")
def read_root():
    return {"text": "Hello World"}