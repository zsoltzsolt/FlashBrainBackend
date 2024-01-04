from pydantic import BaseModel
from typing import List, Optional


class ViewDisplay(BaseModel):
    viewId: Optional[int]
    userId: Optional[int]
    class Config():
        from_attributes = True

class LikeDisplay(BaseModel):
    likeId: Optional[int]
    summaryId: Optional[int]
    userId: Optional[int]
    class Config():
        from_attributes = True

class FlashCardDisplay(BaseModel):
    flashcardId: int 
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
    like: List[LikeDisplay] = []
    viewHistory: List[ViewDisplay] = []
    isPublic: bool
    class Config():
        from_attributes = True

class UserDisplay(BaseModel):
    uid: int
    username: str
    email: str 
    emailVerified: bool
    current_streak: int
    max_streak: int
    score: int
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
    like: Optional[LikeDisplay] = None
    class Config():
        from_attributes = True


class YouTubeBase(BaseModel):
    url: str
    
class Filter(BaseModel):
    categories: List[int]
    query: str