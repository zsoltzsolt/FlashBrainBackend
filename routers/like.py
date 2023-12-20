from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session
from fastapi import Depends
from db.database import get_db
from routers.schemas import UserDisplay
from auth.oauth2 import get_current_user
from db.like import add_like, delete_like
from fastapi.exceptions import HTTPException
from fastapi import status

router = APIRouter(
    prefix = "/like",
    tags = ["Like"]
)

@router.get("/{summaryId}")
def add_new_like(summaryId: int, db: Session = Depends(get_db), user: UserDisplay = Depends(get_current_user)):
    like = add_like(summaryId, db, user)
    return HTTPException(status_code=status.HTTP_201_CREATED, detail = "Like added succesfully!")

@router.delete("/{summaryId}")
def delete_like1(summaryId: int, db: Session = Depends(get_db), user: UserDisplay = Depends(get_current_user)):
    if delete_like(summaryId, db, user) is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Like not found!")
    else:
        return HTTPException(status_code=status.HTTP_200_OK, detail = "Like deleted succesfully!")
    