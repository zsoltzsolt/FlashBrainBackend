from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session
from fastapi import Depends
from db.database import get_db
from routers.schemas import UserDisplay
from auth.oauth2 import get_current_user
from db.like import add_like

router = APIRouter(
    prefix = "/like",
    tags = ["Like"]
)

@router.get("/{summaryId}")
def add_new_like(summaryId: int, db: Session = Depends(get_db), user: UserDisplay = Depends(get_current_user)):
    like = add_like(summaryId, db, user)
    return like
    