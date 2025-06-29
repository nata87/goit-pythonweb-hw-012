from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.auth.security import hash_password, verify_password
from src.auth.jwt import create_access_token
from src.auth.email_service import send_verification_email
from src.settings.config import get_db, settings
from src.database.models import User
from src.schemas.user import UserCreate, UserResponse
from src.services.auth import get_email_from_token, decode_jwt_token, verify_email_token

router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    expires = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # у .env: 30
    token = create_access_token({"sub": new_user.email}, expires)

    await send_verification_email(new_user.email, token)

    return new_user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email}, expires_minutes=60)

    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.confirmed:
        return JSONResponse(content={"message": "Account already verified"})

    user.confirmed = True
    db.commit()
    return JSONResponse(content={"message": "Email successfully verified"})
