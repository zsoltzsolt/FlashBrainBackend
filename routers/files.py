from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from routers.schemas import SummarySourceBase, SummaryBase, UserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
import shutil
from llm.summaryGeneration import PDFSummaryGenerator
import asyncio
from auth.oauth2 import get_current_active_user
from email1.emailSender import send_email
from email1.summaryReady import create_subject_body
from time import sleep
from fastapi import BackgroundTasks
import os

router = APIRouter(
    prefix="/summary/file",
    tags=["Summary"]
)

def create_summary(request: SummarySourceBase,upload_file: UploadFile,db: Session,user: UserDisplay):
    path = f"files/{upload_file.filename}"
    summary = SummaryBase(title="", 
                          ownerId=user.uid, 
                          categoryId=1, 
                          isPublic=request.isPublic, 
                          path=path)
    with open(path, "wb") as output_file:
        shutil.copyfileobj(upload_file.file, output_file)

    
    id1 =PDFSummaryGenerator().generate_summary(summary, db)
    
    sleep(100)
    
    subject, body = create_subject_body(user.username, f"{os.environ.get('FRONTEND_URL')}/viewflashcard/{id1}")
    
    send_email(user.email, subject, body)


@router.post("")
def getFile(
    background_tasks: BackgroundTasks,
    request: SummarySourceBase = Depends(),
    upload_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: UserDisplay = Depends(get_current_active_user)
):
    background_tasks.add_task(create_summary, request, upload_file, db, user)
    return {"message": "Merry Christmas Radu"}

