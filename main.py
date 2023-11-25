from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user
from auth import authentication
app = FastAPI()

app.include_router(user.router)
app.include_router(authentication.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

models.Base.metadata.create_all(engine)