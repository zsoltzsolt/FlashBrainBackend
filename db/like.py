from sqlalchemy.orm.session import Session
from routers.schemas import UserDisplay
from db.models import DbLike
from sqlalchemy import and_

def add_like(summaryId: int, db: Session, user: UserDisplay):
    new_like = DbLike(
        userId = user.uid,
        summaryId = summaryId
    )
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like

def delete_like(summaryId: int, db: Session, user: UserDisplay):
    like = db.query(DbLike).filter(
        and_(
            summaryId == DbLike.summaryId, 
            user.uid == DbLike.userId)
        ).first()
    if like:
        db.delete(like)
        db.commit()
        return "ok"
    return None
    
    

    
    
    