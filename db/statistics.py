from fastapi import FastAPI, BackgroundTasks, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import DbUser
from routers.schemas import UserDisplay
from db.like import get_liked_summaries
from db.user import update_streak
from db.user import calculate_score
from email1.statistics import send_statistics
from email1.emailSender import send_email
from email1.missYou import send_missing_you_email

def schedule_summary_messages_task():
    
    print("Send mail")
    
    with SessionLocal() as db:
            users = db.query(DbUser).all()
            for user in users:
                user.liked_summaries = get_liked_summaries(db, user)
                user_updated = update_streak(user)
                score = calculate_score(user_updated.uid, db)
                user_details = UserDisplay(
                                uid=user_updated.uid,
                                username=user_updated.username,
                                email=user_updated.email,
                                emailVerified=user_updated.emailVerified,
                                current_streak=user_updated.current_streak,
                                max_streak=user_updated.max_streak,
                                score=score,
                                summaries=user_updated.summaries
                                )
                print(user_updated.login_history[-1].loginDate)
                no_days_since_last_login = (datetime.utcnow() - user_updated.login_history[-1].loginDate).days
                if no_days_since_last_login > 2:
                    subject, body = send_missing_you_email(user = user_details, no_days=no_days_since_last_login)
                else:
                    subject, body = send_statistics(user = user_details)
                send_email(user_updated.email, subject, body)