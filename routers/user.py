from fastapi.routing import APIRouter
from routers.schemas import UserDisplay
from db.database import get_db
from sqlalchemy.orm.session import Session
from fastapi import Depends
from routers.schemas import UserBase
from db.user import create_user_func, update_streak
import sqlalchemy
from sqlalchemy import func
from fastapi import HTTPException
from fastapi import status
from auth.oauth2 import get_current_active_user
from db.user import get_user_by_id
from typing import Union, Optional
from pydantic import BaseModel
from fastapi.openapi.models import HTTPBase
from db.models import DbUser, DbSummary, DbLike, DbSummaryViewHistory



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
    
@router.get('/leaderboard')
def users_sorted_by_score(db: Session = Depends(get_db)):
    try:
        users = db.query(DbUser).all()

        user_scores = []
        for user in users:
            summaries = db.query(DbSummary).filter(DbSummary.owner == user).all()
            total_score = 0
            for summary in summaries:
                likes_count = db.query(func.count(DbLike.likeId)).filter(DbLike.summary == summary).scalar()
                views_count = db.query(func.count(DbSummaryViewHistory.viewId)).filter(DbSummaryViewHistory.summary == summary).scalar()
                summary_score = likes_count * 10 + 10 * views_count
                total_score += summary_score
            user_scores.append({"uid": user.uid, "username": user.username, "score": total_score})

        sorted_users = sorted(user_scores, key=lambda x: x["score"], reverse=True)

        return sorted_users

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/{uid}", response_model=UserDisplay)
def get_user_by_id1(uid: int, db: Session = Depends(get_db)):
    user = get_user_by_id(uid, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {uid} not found!")
    else:
        return user
    


    


        
