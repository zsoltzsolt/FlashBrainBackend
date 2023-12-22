from fastapi import APIRouter
from routers.schemas import SummarySourceBase, YouTubeBase, SummaryBase, UserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from fastapi import Depends
from fastapi import Body
from llm.summaryGeneration import YoutubeSummaryGenerator
from auth.oauth2 import get_current_active_user
from email1.emailSender import send_email
from email1.summaryReady import create_subject_body
from time import sleep
from fastapi import BackgroundTasks

router = APIRouter(
    prefix="/summary/video",
    tags=["Summary"]
)

def getIdFromUrl(url):
    return url.split("/")[-1]

def create_summary( youtube: YouTubeBase,request: SummarySourceBase,db: Session,user: UserDisplay):
    
    summary = SummaryBase(title="", 
                          ownerId=user.uid, 
                          categoryId=1, 
                          isPublic=request.isPublic, 
                          path=youtube.url)
    
    id1 = YoutubeSummaryGenerator().generate_summary(summary, db)
    
    sleep(100)
    
    subject, body = create_subject_body(user.username, f"localhost:3000/summaries/{id1}")
    
    send_email(user.email, subject, body)
    

@router.post("/")
async def getVideo(
    background_tasks: BackgroundTasks,
    youtube: YouTubeBase,
    request: SummarySourceBase = Depends(),
    db: Session = Depends(get_db),
    user: UserDisplay = Depends(get_current_active_user)
):
    background_tasks.add_task(create_summary, youtube, request, db, user)
    return {"message": "Merry Christmas Radu"}

