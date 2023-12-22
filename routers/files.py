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

router = APIRouter(
    prefix="/summary/file",
    tags=["Summary"]
)


@router.post("/")
def getFile(
    request: SummarySourceBase = Depends(),
    upload_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: UserDisplay = Depends(get_current_active_user)
):
    path = f"files/{upload_file.filename}"
    summary = SummaryBase(title="", 
                          ownerId=user.uid, 
                          categoryId=1, 
                          isPublic=request.isPublic, 
                          path=path)
    with open(path, "wb") as output_file:
        shutil.copyfileobj(upload_file.file, output_file)

    
    result =PDFSummaryGenerator().generate_summary(summary, db, user)
    
    sleep(300)
    
    subject, body = create_subject_body(user.username, f"localhost:3000/summaries/")
    
    send_email(user.email, subject, body)
    
    return result

