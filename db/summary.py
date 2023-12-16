from routers.schemas import SummaryBase, FlashCardBase, SummarySourceBase
import json
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from llm.summaryGeneration import generate_metadata, generate_summaries
from db.models import DbSummary
from db.flashcard import create_flash_card
from sqlalchemy.orm import joinedload

def generate_summary(request: SummarySourceBase, db: Session = Depends(get_db)):
    
    title_category = generate_metadata(request.path)
    print(title_category)
    newJsonMeta = json.loads(title_category)
    
    message = generate_summaries(request.path)
    newJson = json.loads(message)
    print(newJson)
    
    new_summary = DbSummary(
        title = newJsonMeta["title"],
        ownerId = request.ownerId,
        categoryId = newJsonMeta["category"],
        isPublic = request.isPublic
    )
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)

    for json_item in newJson:
        new_flash = FlashCardBase(
            title=json_item['title'],
            content=json_item['content'],
            imagePath="https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fsearch%3Fk%3Dexample&psig=AOvVaw0PcUbcIpaFBbAF-M_4Qgnq&ust=1702793939676000&source=images&cd=vfe&ved=0CBIQjRxqFwoTCJDQ8fKnk4MDFQAAAAAdAAAAABAJ",
            summaryId=new_summary.summaryId
        )
        create_flash_card(new_flash, db)
    
    return new_summary

def get_all(db: Session):
    return db.query(DbSummary).all()