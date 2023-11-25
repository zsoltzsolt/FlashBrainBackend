from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class UserDisplay(UserBase):
    uid: int
    name: str
    email: str 
    class Config():
        orm_mode = True