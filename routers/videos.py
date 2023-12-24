import re
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from routers.schemas import SummarySourceBase, YouTubeBase, SummaryBase, UserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from llm.summaryGeneration import YoutubeSummaryGenerator
from auth.oauth2 import get_current_active_user
from email1.emailSender import send_email
from email1.summaryReady import create_subject_body
from time import sleep
import re

router = APIRouter(
    prefix="/summary/video",
    tags=["Summary"]
)

import re

def extract_youtube_video_id(url: str):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    youtube_match = re.match(youtube_regex, url)
    
    if youtube_match:
        video_id = youtube_match.group(6)
        return video_id
    else:
        return None



def is_valid_youtube_url(url: str):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    youtube_match = re.match(youtube_regex, url)
    return youtube_match is not None

def create_summary(youtube: YouTubeBase, request: SummarySourceBase, db: Session, user: UserDisplay):

    summary = SummaryBase(
        title="",
        ownerId=user.uid,
        categoryId=1,
        isPublic=request.isPublic,
        path=extract_youtube_video_id(youtube.url)
    )

    id1 = YoutubeSummaryGenerator().generate_summary(summary, db)

    sleep(100)

    subject, body = create_subject_body(user.username, f"localhost:3000/summaries/{id1}\n")

    send_email(user.email, subject, body)

@router.post("")
async def getVideo(
    background_tasks: BackgroundTasks,
    youtube: YouTubeBase,
    request: SummarySourceBase = Depends(),
    db: Session = Depends(get_db),
    user: UserDisplay = Depends(get_current_active_user)
):
     if not is_valid_youtube_url(youtube.url):
        raise HTTPException(status_code=422, detail="Invalid YouTube URL")
     else:
        background_tasks.add_task(create_summary, youtube, request, db, user)
        return {"message": "Merry Christmas Radu"}
