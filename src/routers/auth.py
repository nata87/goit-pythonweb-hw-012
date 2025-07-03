from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.user import RequestResetPassword, ResetPassword
from src.auth.reset import create_reset_token, verify_reset_token
from src.repository.users import get_user_by_email, update_user_password
from src.auth.security import hash_password
from src.services.email import send_reset_password_email
from sqlalchemy.orm import Session
from src.settings.config import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/reset-password-request")
async def reset_password_request(
    request_data: RequestResetPassword, db: Session = Depends(get_db)
):
    user = get_user_by_email(request_data.email, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_reset_token(user.email)
    try:
        await send_reset_password_email(user.email, token)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send reset email")

    return {"message": "Password reset email sent"}


@router.post("/reset-password")
async def reset_password(reset_data: ResetPassword, db: Session = Depends(get_db)):
    email = verify_reset_token(reset_data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_pwd = hash_password(reset_data.new_password)
    update_user_password(email, hashed_pwd, db)

    return {"message": "Password updated successfully"}