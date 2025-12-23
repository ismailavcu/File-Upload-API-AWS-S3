import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.routes.users import get_db
from app.models import File as FileModel
from app.auth import get_current_user
from app.models import User
from app.services.s3 import upload_file_to_s3

router = APIRouter(prefix="/files", tags=["Files"])

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_TYPES = ["image/png", "image/jpeg", "image/jpg", "application/pdf"]


@router.post("/upload")
async def upload_file(
    uploaded_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if uploaded_file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await uploaded_file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    s3_key = upload_file_to_s3(
        file_bytes=contents,
        content_type=uploaded_file.content_type,
        user_id=current_user.id
    )

    new_file = FileModel(
        filename=uploaded_file.filename,
        content_type=uploaded_file.content_type,
        size = uploaded_file.size,
        s3_key=s3_key,
        owner_id=current_user.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "message": "File uploaded to S3",
        "file_id": new_file.id
    }

