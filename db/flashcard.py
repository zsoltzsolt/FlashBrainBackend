from sqlalchemy.orm.session import Session
from routers.schemas import FlashCardBase
from db.models import DbFlashCard

def create_flash_card(request:FlashCardBase, db: Session):
    new_flashcard = DbFlashCard(
        title = request.title,
        content = request.content,
        imagePath = request.imagePath,
        summary_id = request.summaryId 
        
    )
    db.add(new_flashcard)
    db.commit()
    db.refresh(new_flashcard)
    return new_flashcard