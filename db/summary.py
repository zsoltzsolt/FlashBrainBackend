from sqlalchemy.orm import Session
from db.models import DbSummary

def get_all(db: Session):
    return db.query(DbSummary).all()