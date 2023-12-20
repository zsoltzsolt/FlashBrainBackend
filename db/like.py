from sqlalchemy.orm.session import Session
from routers.schemas import UserDisplay
from db.models import DbLike

def add_like(summaryId: int, db: Session, user: UserDisplay):
    new_like = DbLike(
        userId = user.uid,
        summaryId = summaryId
    )
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like
    

    
    
    