from fastapi.routing import APIRouter
from routers.schemas import UserLogin, UserBase, UserDisplay
from sqlalchemy.orm.session import Session
from fastapi import Depends
from db.database import get_db
from db.models import DbUser
from fastapi.exceptions import HTTPException
from fastapi import status
from db.hashing import Hash
from auth.oauth2 import create_access_token
from datetime import timedelta
from auth.oauth2 import get_current_user
from auth.oauth2 import get_current_active_user


router = APIRouter(
    prefix="/auth",
    tags=["User"]
)

@router.post("/token")
def generate_token(request: UserLogin, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    elif not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is not correct!")

    access_token = create_access_token(data={'sub': user.username}, expires_delta=timedelta(minutes=60))

    return {
        'accessToken': access_token
    }
    
@router.get("/token/status", response_model=UserDisplay)
def verify_token(db:Session = Depends(get_db), user:UserBase = Depends(get_current_active_user)):
    return user  