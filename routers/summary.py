from fastapi import APIRouter
from db.summary import get_all, delete_summary, filter_summary
from db.database import get_db
from sqlalchemy.orm.session import Session
from fastapi import Depends
from routers.schemas import SummaryDisplay, Filter
from typing import List
from routers.schemas import UserDisplay
from auth.oauth2 import get_current_active_user
from fastapi.exceptions import HTTPException
from fastapi import status

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)

@router.get("/all", response_model=List[SummaryDisplay])
def get_all_summaries(db: Session = Depends(get_db)):
    return get_all(db)

@router.delete("/{summaryId}")
def delete_summary1(summaryId: int, db: Session = Depends(get_db), user: UserDisplay = Depends(get_current_active_user)):
    if delete_summary(summaryId, db, user) is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Summary with id {summaryId} not found!")
    else:
        return HTTPException(status_code=status.HTTP_200_OK, detail = f"Summary with id {summaryId} deleted succesfully!")
    
@router.post("/filtered",response_model=List[SummaryDisplay])
def get_all_filtered(filter1: Filter, db: Session = Depends(get_db)):
    return filter_summary(filter1, db)