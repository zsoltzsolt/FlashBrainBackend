from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import user
from jose import JWTError, jwt
from db.models import DbLoginHistory


oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth')

SECRET_KEY = 'db5595cb359246dbb9858d451a4132b32f1a263a7fb06f12f89eb2a3f94bfe30'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
     credentials_exception = HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Could not validate credentials",
         headers={"WWW-Authenticate": "Bearer"}
     )
     try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         username: str = payload.get("sub")
         if username is None:
             raise credentials_exception
     except JWTError:
         raise credentials_exception

     user1 = user.get_user_by_username(db, username)

     if user1 is None:
         raise credentials_exception

     return user1
 
def get_current_active_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    if current_user.emailVerified == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email is not verified!")
    
    return current_user





