from fastapi import APIRouter
from db.summary import get_all
from db.database import get_db
from sqlalchemy.orm.session import Session
from fastapi import Depends
from routers.schemas import SummaryDisplay
from typing import List

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)

@router.get("/all", response_model=List[SummaryDisplay])
def get_all_summaries(db: Session = Depends(get_db)):
    return get_all(db)