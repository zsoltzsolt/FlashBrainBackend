from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    uid: int
    username: str
    email: str 
    class Config():
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str