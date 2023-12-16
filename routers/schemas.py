from pydantic import BaseModel
from typing import List, Optional

class FlashCardDisplay(BaseModel):
    title: str
    content: str
    imagePath: str
    summaryId: int
    class Config():
        from_attributes = True

class SummaryDisplay(BaseModel):
    summaryId: int
    title: str
    ownerId: int
    categoryId: int
    flashcards: List[FlashCardDisplay] = []
    isPublic: bool
    class Config():
        from_attributes = True

class UserDisplay(BaseModel):
    uid: int
    username: str
    email: str 
    emailVerified: bool
    summaries: List[SummaryDisplay] = []
    class Config():
        from_attributes = True
        
class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
    
class SummarySourceBase(BaseModel):
    ownerId: int
    isPublic: bool
    
class SummaryBase(BaseModel):
    title: str
    ownerId: int
    categoryId: int
    isPublic: bool
    path: str
    
class FlashCardBase(BaseModel):
    title: str
    content: str
    imagePath: str
    summaryId: int
    class Config():
        from_attributes = True


class YouTubeBase(BaseModel):
    url: str