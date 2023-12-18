from fastapi import APIRouter
from routers.schemas import SummarySourceBase, YouTubeBase, SummaryBase
from sqlalchemy.orm.session import Session
from db.database import get_db
from fastapi import Depends
from fastapi import Body
from llm.summaryGeneration import YoutubeSummaryGenerator


router = APIRouter(
    prefix="/video",
    tags=["Video"]
)

@router.post("/")
def getVideo(
    youtube: YouTubeBase,
    request: SummarySourceBase = Depends(),
    db: Session = Depends(get_db)
):
    summary = SummaryBase(title="", 
                          ownerId=request.ownerId, 
                          categoryId=1, 
                          isPublic=request.isPublic, 
                          path=youtube.url)
    return YoutubeSummaryGenerator().generate_summary(summary, db)