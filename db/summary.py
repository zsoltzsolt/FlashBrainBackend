from sqlalchemy.orm import Session
from db.models import DbSummary
from routers.schemas import UserDisplay
from db.models import DbSummary
from sqlalchemy import and_

def get_all(db: Session):
    return db.query(DbSummary).all()

def delete_summary(summaryId: int, db: Session, user: UserDisplay):
    like = db.query(DbSummary).filter(
        and_(
            summaryId == DbSummary.summaryId, 
            user.uid == DbSummary.ownerId)
        ).first()
    if like:
        db.delete(like)
        db.commit()
        return "ok"
    return None
    