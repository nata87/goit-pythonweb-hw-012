from src.database.models import User
from sqlalchemy.orm import Session


def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()

def update_user_password(email: str, hashed_password: str, db: Session) -> None:
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.hashed_password = hashed_password
        db.commit()
        db.refresh(user)
