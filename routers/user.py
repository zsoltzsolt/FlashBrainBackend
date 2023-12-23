from fastapi.routing import APIRouter
from routers.schemas import UserDisplay
from db.database import get_db
from sqlalchemy.orm.session import Session
from fastapi import Depends
from routers.schemas import UserBase
from db.user import create_user_func, update_streak
from db.like import get_liked_summaries
from db.database import SessionLocal
import sqlalchemy
from fastapi import HTTPException
from fastapi import status
from datetime import timedelta
from auth.oauth2 import create_access_token
from auth.oauth2 import get_current_active_user
from typing import List
from routers.schemas import SummaryDisplay


router = APIRouter(
    prefix = "/user",
    tags = ["User"]
)

@router.post("/")
def create_user(request: UserBase, db: Session = Depends(get_db)):
    try:
        access_token = create_user_func(db, request)

    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already in use")

    return {
        'access_token': access_token
    }
    
@router.get("/streak")
def get_daily_streak(user: UserDisplay = Depends(get_current_active_user)):
    return update_streak(user)

@router.get("/favourites", response_model=List[SummaryDisplay])
def get_liked_summaries1(db: Session = Depends(get_db), user: UserDisplay = Depends(get_current_active_user)):
    return get_liked_summaries(db, user)