from fastapi import APIRouter
from fastapi import UploadFile, File, Depends
from routers.schemas import SummarySourceBase, SummaryBase
from sqlalchemy.orm.session import Session
from db.database import get_db
import shutil
from db.summary import generate_summary

router = APIRouter(
    prefix="/file",
    tags=["File"]
)

@router.post("/")
def getFile(
    request: SummarySourceBase = Depends(),
    uploadFile: UploadFile = File(...),
    db: Session = Depends(get_db)
    ):
    path = f"files/{uploadFile.filename}"
    
    with open(path, "wb") as outputFile:
        shutil.copyfileobj(uploadFile.file, outputFile)
    summary = SummaryBase(title="", 
                          ownerId=request.ownerId, 
                          categoryId=1, 
                          isPublic=request.isPublic, 
                          path=path)
    return generate_summary(summary, db)
    
    
