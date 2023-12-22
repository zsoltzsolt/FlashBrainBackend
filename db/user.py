from sqlalchemy.orm.session import Session
from routers.schemas import UserBase, UserDisplay
from db.models import DbUser, DbLoginHistory
from db.database import SessionLocal
from db.hashing import Hash
from email1.emailConfirmationData import create_subject_body
from email1.emailSender import send_email
from auth.oauth2 import create_access_token
import os
from datetime import datetime, timedelta
from sqlalchemy import desc

def create_user_func(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.hash_password(request.password)
    )
    db.add(new_user)
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


def update_streak(user):
    # Access the login_history attribute directly
    login_history = user.login_history

    if not login_history:
        # No login history, reset streaks
        user.current_streak = 1
        user.max_streak = 1
    else:
        # Order login history by login date in descending order
        login_history_ordered = sorted(login_history, key=lambda x: x.loginDate, reverse=True)

        today = datetime.utcnow().date()
        last_login_date = login_history_ordered[0].loginDate.date()

        if (today - last_login_date).days == 1:
            # Increment current streak
            user.current_streak += 1
            user.max_streak = max(user.current_streak, user.max_streak)
        elif (today - last_login_date).days > 1:
            # Reset streaks
            user.current_streak = 1
            user.max_streak = max(user.current_streak, user.max_streak)

    return {
        "current_streak": user.current_streak,
        "max_streak": user.max_streak,
    }
