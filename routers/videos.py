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

def getIdFromUrl(url):
    return url.split("/")[-1]

@router.post("/")
async def getVideo(
    youtube: YouTubeBase,
    request: SummarySourceBase = Depends(),
    db: Session = Depends(get_db)
):
    # We get the url but we need to get the id
     
    summary = SummaryBase(title="", 
                          ownerId=request.ownerId, 
                          categoryId=1, 
                          isPublic=request.isPublic, 
                          path=youtube.url)
    result = await YoutubeSummaryGenerator().generate_summary(summary, db)
    return result
