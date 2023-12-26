from fastapi.routing import APIRouter
from fastapi import Depends
from db.database import get_db
from sqlalchemy.orm.session import Session
from fastapi.params import Query
from auth.oauth2 import get_current_user
from routers.schemas import UserDisplay
from fastapi.responses import RedirectResponse
import os

router = APIRouter( 
    prefix = "/email", 
    tags = ["Email"] 
    )

@router.get("/")
async def email(token: str, db:Session = Depends(get_db)):
    user = get_current_user(token, db)
    user.emailVerified = True
    db.commit()
    db.refresh(user)
    return RedirectResponse(os.environ.get('FRONTEND_URL'), status_code=302)