from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class DbUser(Base):
     __tablename__ = "user"
     uid = Column(Integer, index=True, primary_key=True)
     username = Column(String, unique=True)
     email = Column(String, unique=True)
     password = Column(String)
     email_verified = Column(Boolean, default=False)
     summaries = relationship("DbSummary", back_populates="owner")
     
class DbCategory(Base):
    __tablename__ = "category"
    category_id = Column(Integer, index=True, primary_key=True)
    category_name = Column(String)
    summaries = relationship("DbSummary", back_populates="category")
  
class DbSummary(Base):
    __tablename__ = "summary"
    summary_id = Column(Integer, index=True, primary_key=True)
    title = Column(String)
    is_public = Column(Boolean)
    category_id = Column(Integer, ForeignKey("category.category_id"))
    owner_id = Column(Integer, ForeignKey("user.uid"))
    owner = relationship("DbUser", back_populates="summaries")  
    category = relationship("DbCategory", back_populates="summaries")
    flashcards = relationship("DbFlashCard", back_populates="summary")
    
class DbFlashCard(Base):
    __tablename__ = "flashcard"
    flashcard_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    imagePath = Column(String)
    summary_id = Column(Integer, ForeignKey("summary.summary_id"))
    summary = relationship("DbSummary", back_populates="flashcards")
     