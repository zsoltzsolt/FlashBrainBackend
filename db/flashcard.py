from sqlalchemy.orm.session import Session
from routers.schemas import FlashCardBase
from db.models import DbFlashCard
from db.database import get_db
from fastapi import Depends

def create_flash_card(request:FlashCardBase, db: Session = Depends(get_db)):
    new_flashcard = DbFlashCard(
        title = request.title,
        content = request.content,
        imagePath = request.imagePath,
        summaryId = request.summaryId 
        
    )
    db.add(new_flashcard)
    db.commit()
    db.refresh(new_flashcard)
    return new_flashcard