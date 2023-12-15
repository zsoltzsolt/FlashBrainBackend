from routers.schemas import SummaryBase, FlashCardBase, SummarySourceBase
import json
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from llm.summaryGeneration import generate_metadata, generate_summaries
from db.models import DbSummary, DbFlashCard

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
    return new_summary