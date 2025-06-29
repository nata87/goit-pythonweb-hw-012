from fastapi import APIRouter, UploadFile, File, Depends
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException

from src.settings.config import settings, get_db
from src.auth.dependencies import get_current_user
from src.database.models import User
from src.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


cloudinary.config(
    cloud_name=settings.CLOUDINARY_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


@router.get("/me", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


from fastapi import UploadFile, File, HTTPException
import cloudinary.uploader

@router.patch("/avatar")
def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        result = cloudinary.uploader.upload(file.file, folder="avatars")
        url = result.get("secure_url")

        if not url:
            raise HTTPException(status_code=500, detail="Failed to upload avatar to Cloudinary")

        current_user.avatar_url = url
        db.commit()
        db.refresh(current_user)

        return {"avatar_url": url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Avatar upload error: {str(e)}")

