from fastapi import APIRouter
from routers.schemas import SummarySourceBase, YouTubeBase, SummaryBase, UserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from fastapi import Depends
from fastapi import Body
from llm.summaryGeneration import YoutubeSummaryGenerator
from auth.oauth2 import get_current_active_user

router = APIRouter(
    prefix="/summary/video",
    tags=["Summary"]
)

def getIdFromUrl(url):
    return url.split("/")[-1]

@router.post("/")
async def getVideo(
    youtube: YouTubeBase,
    request: SummarySourceBase = Depends(),
    db: Session = Depends(get_db),
    user: UserDisplay = Depends(get_current_active_user)
):
    # We get the url but we need to get the id
     
    summary = SummaryBase(title="", 
                          ownerId=user.uid, 
                          categoryId=1, 
                          isPublic=request.isPublic, 
                          path=youtube.url)
    result = await YoutubeSummaryGenerator().generate_summary(summary, db)
    return result
