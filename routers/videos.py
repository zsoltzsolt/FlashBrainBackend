from fastapi import APIRouter
from routers.schemas import SummarySourceBase, YouTubeBase
from sqlalchemy.orm.session import Session
from db.database import get_db
from fastapi import Depends
from fastapi import Body

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
    return {
        "message" : f"Video uploaded successfully : {youtube.url}" 
    }