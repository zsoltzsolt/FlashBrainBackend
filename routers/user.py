from fastapi.routing import APIRouter
from routers.schemas import UserDisplay
from db.database import get_db
from sqlalchemy.orm.session import Session
from fastapi import Depends
from routers.schemas import UserBase
from db.user import create_user_func, update_streak
import sqlalchemy
from fastapi import HTTPException
from fastapi import status
from auth.oauth2 import get_current_active_user
from db.user import get_user_by_id



router = APIRouter(
    prefix = "/user",
    tags = ["User"]
)

@router.post("/")
def create_user(request: UserBase, db: Session = Depends(get_db)):
    try:
        access_token = create_user_func(db, request)

    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already in use")

    return {
        'access_token': access_token
    }
    
@router.get("/streak")
def get_daily_streak(user: UserDisplay = Depends(get_current_active_user)):
    return update_streak(user)

@router.get("/{uid}", response_model=UserDisplay)
def get_user_by_id1(uid: int, db: Session = Depends(get_db)):
    user = get_user_by_id(uid, db)
    if user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id {uid} not found!")
    else:
        return user
        
