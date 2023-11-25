from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user

app = FastAPI()

app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}