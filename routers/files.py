from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from routers.schemas import SummarySourceBase, SummaryBase, UserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
import shutil
from llm.summaryGeneration import PDFSummaryGenerator
import asyncio
from auth.oauth2 import get_current_active_user

router = APIRouter(
    prefix="/summary/file",
    tags=["Summary"]
)

async def process_file(summary, upload_file, db):
    result = await PDFSummaryGenerator().generate_summary(summary, db)
    return {"ok": "ok"}

@router.post("/")
async def getFile(
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
    try:
        # Utilizăm asyncio.wait_for pentru a gestiona timeout-ul de 20 de secunde
        result = await asyncio.wait_for(process_file(summary, upload_file, db), timeout=20)
        return result
    except asyncio.TimeoutError:
        # Răspunsul pentru timeout
        return JSONResponse(content={"error": "Timeout reached"}, status_code=200)
