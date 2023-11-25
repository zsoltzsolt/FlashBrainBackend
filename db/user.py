from sqlalchemy.orm.session import Session
from routers.schemas import UserBase, UserDisplay
from db.models import DbUser
from db.database import SessionLocal
from db.hashing import Hash
from email1.emailConfirmationData import create_subject_body
from email1.emailSender import send_email
from auth.oauth2 import create_access_token
import os

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
    link = os.environ.get("HOST_URL") + "email?token=" + access_token
    subject, body = create_subject_body(request.username, link)
    send_email(request.email, subject, body)

    return access_token

def get_user_by_username(db: Session, username: str):
     user = db.query(DbUser).filter(DbUser.username == username).first()
     return user