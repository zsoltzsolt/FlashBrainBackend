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


def update_streak(user):
    login_history = user.login_history

    if not login_history:
        # No login history, reset streaks
        user.current_streak = 1
        user.max_streak = 1
    else:
        # Order login history by login date in descending order
        login_history_ordered = sorted(login_history, key=lambda x: x.loginDate, reverse=True)
        
        today = datetime.utcnow().date()
        new_streak = 1

        # Iterăm prin istoricul de logări și numărăm zilele consecutive începând de la ziua curentă
        for login in login_history_ordered:
            login_date = login.loginDate.date()


            if (today - login_date).days == 1:
                # Dacă este ziua precedentă, continuăm șirul curent
                new_streak += user.current_streak
                break
            

        # Actualizăm streak-urile
        user.current_streak = new_streak
        user.max_streak = max(new_streak, user.max_streak)
        
        return user

