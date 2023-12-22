from sqlalchemy.orm import Session
from db.models import DbSummary
from routers.schemas import UserDisplay, Filter
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

def filter_summary(filer1: Filter, db: Session):
    #print(f"{filer1.query} si {filer1.categories}")
    if len(filer1.categories) > 0:
        if filer1.categories[0] == 1:
            return db.query(DbSummary).filter(DbSummary.title.ilike(f"%{filer1.query}%"))
    return db.query(DbSummary).filter(
         and_(
                DbSummary.categoryId.in_(filer1.categories),
            DbSummary.title.ilike(f"%{filer1.query}%")
            )
     ).all()
    