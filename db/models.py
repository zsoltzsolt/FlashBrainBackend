from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class DbUser(Base):
     __tablename__ = "user"
     uid = Column(Integer, index=True, primary_key=True)
     username = Column(String, unique=True)
     email = Column(String, unique=True)
     password = Column(String)
     emailVerified = Column(Boolean, default=False)
     summaries = relationship("DbSummary", back_populates="owner", lazy="joined")
     likes = relationship('DbLike', back_populates='user')
     login_history = relationship('DbLoginHistory', back_populates='user')

class DbLoginHistory(Base):
    __tablename__ = "login_history"
    loginId = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('user.uid'))
    user = relationship('DbUser', back_populates='login_history')
    loginDate = Column(DateTime, default=datetime.utcnow)
     
class DbCategory(Base):
    __tablename__ = "category"
    categoryId = Column(Integer, index=True, primary_key=True)
    categoryName = Column(String)
    summaries = relationship("DbSummary", back_populates="category")
  
class DbSummary(Base):
    __tablename__ = "summary"
    summaryId = Column(Integer, index=True, primary_key=True)
    title = Column(String)
    isPublic = Column(Boolean)
    categoryId = Column(Integer, ForeignKey("category.categoryId"))
    ownerId = Column(Integer, ForeignKey("user.uid"))
    owner = relationship("DbUser", back_populates="summaries")  
    category = relationship("DbCategory", back_populates="summaries")
    flashcards = relationship('DbFlashCard', back_populates='summary')
    like = relationship('DbLike', back_populates="summary")

    
class DbFlashCard(Base):
    __tablename__ = "flashcard"
    flashcardId = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    imagePath = Column(String)
    summaryId = Column(Integer, ForeignKey('summary.summaryId'))
    summary = relationship('DbSummary', back_populates='flashcards')
     
class DbLike(Base):
    __tablename__ = "like"
    likeId = Column(Integer, primary_key=True, autoincrement=True)
    summaryId = Column(Integer, ForeignKey('summary.summaryId'))
    summary = relationship('DbSummary', back_populates='like')
    userId = Column(Integer, ForeignKey('user.uid'))
    user = relationship('DbUser', back_populates='likes')