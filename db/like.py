from sqlalchemy.orm.session import Session
from routers.schemas import UserDisplay
from db.models import DbLike, DbSummary
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

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
 
def get_liked_summaries(db: Session, user: UserDisplay):
 
    liked_summaries = db.query(DbSummary).\
    join(DbLike, DbLike.summaryId == DbSummary.summaryId).\
    filter(DbLike.userId == user.uid).\
    options(joinedload(DbSummary.owner)).all()

    return liked_summaries  
    

    
    
    