from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    uid = Column(Integer, index=True, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)