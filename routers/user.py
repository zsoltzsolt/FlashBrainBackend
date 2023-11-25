from fastapi.routing import APIRouter
from routers.schemas import UserDisplay
from db.database import get_db
from sqlalchemy.orm.session import Session
from fastapi import Depends
from routers.schemas import UserBase
from db.user import create_user_func
from db.database import SessionLocal
import sqlalchemy
from fastapi import HTTPException
from fastapi import status
from datetime import timedelta
from auth.oauth2 import create_access_token


router = APIRouter(
    prefix = "/user",
    tags = ["User"]
)

@router.post("/")
def create_user(request: UserBase, db: Session = Depends(get_db)):
    try:
        user = create_user_func(db, request)

    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already in use")

    access_token = create_access_token(data={'sub': user.username}, expires_delta=timedelta(minutes=60))

    return {
        'access_token': access_token
    }