from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user, email, files, videos, summary
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(email.router)
app.include_router(files.router)
app.include_router(videos.router)
app.include_router(summary.router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

models.Base.metadata.create_all(engine)