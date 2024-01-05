from sqlalchemy.orm.session import Session
from routers.schemas import UserBase, UserDisplay
from db.models import DbUser, DbLoginHistory, DbSummary, DbLike, DbSummaryViewHistory
from db.database import SessionLocal
from db.hashing import Hash
from email1.emailConfirmationData import create_subject_body
from email1.emailSender import send_email
from auth.oauth2 import create_access_token
import os
from datetime import datetime, timedelta
from sqlalchemy import desc
from fastapi.exceptions import HTTPException
from sqlalchemy import func
from datetime import datetime

def create_user_func(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.hash_password(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    login_entry = DbLoginHistory(user=new_user)
    db.add(login_entry)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.username})
    access_token = create_access_token(data={"sub": new_user.username})
    link = os.environ.get("HOST_URL") + "email?token=" + access_token
    subject, body = create_subject_body(request.username, link)
    send_email(request.email, subject, body)

    return access_token

def get_user_by_username(db: Session, username: str):
     user = db.query(DbUser).filter(DbUser.username == username).first()
     return user
 
def get_user_by_id(id: int, db: Session) -> UserDisplay:
     return db.query(DbUser).get(id)


def update_streak(user, db: Session):
    login_history = user.login_history

    if not login_history:
        user.current_streak = 1
        user.max_streak = 1
    elif (login_history[-2].login_date - datetime.utcnow()) == 0:
        return 
    else:
        login_history_ordered = sorted(login_history, key=lambda x: x.loginDate, reverse=True)
        
        today = datetime.utcnow().date()
        new_streak = 1

        for login in login_history_ordered:
            login_date = login.loginDate.date()


            if (today - login_date).days == 1:
                new_streak += user.current_streak
                break
            

        user.current_streak = new_streak
        user.max_streak = max(new_streak, user.max_streak)
        
        db.commit()
        
        return user
    
def calculate_score(user_id: int, db: Session):
    
    try:
        # Query the database to get the user, their summaries, likes, and views
        user = db.query(DbUser).get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        summaries = db.query(DbSummary).filter(DbSummary.owner == user).all()

        # Calculate the score based on the number of likes and views for each summary
        total_score = 0
        for summary in summaries:
            likes_count = db.query(func.count(DbLike.likeId)).filter(DbLike.summary == summary).scalar()
            views_count = db.query(func.count(DbSummaryViewHistory.viewId)).filter(DbSummaryViewHistory.summary == summary).scalar()
            summary_score = likes_count * 10 + 10 * views_count
            total_score += summary_score

        return total_score
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

