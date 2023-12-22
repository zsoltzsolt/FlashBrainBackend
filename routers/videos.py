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

router = APIRouter(
    prefix="/summary/video",
    tags=["Summary"]
)

def getIdFromUrl(url):
    return url.split("/")[-1]

@router.post("/")
def getVideo(
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
    id1 = YoutubeSummaryGenerator().generate_summary(summary, db)
    
    sleep(300)
    
    subject, body = create_subject_body(user.username, f"localhost:3000/summaries/{id1}")
    
    send_email(user.email, subject, body)
    
    return {"response": "Summary generated succesfully!"}
