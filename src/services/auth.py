from jose import jwt, JWTError
from fastapi import HTTPException, status
from src.settings.config import SECRET_KEY, ALGORITHM


def verify_email_token(token: str) -> str | None:
    """
    Verify a JWT token used for email confirmation and extract the subject (email).

    :param token: JWT token received from the user
    :return: The email (subject) if token is valid, otherwise None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def get_email_from_token(token: str) -> str:
    """
    Extract the email from a valid JWT token, or raise an HTTPException if invalid.

    :param token: JWT access token
    :return: Email extracted from the token
    :raises HTTPException: If the token is invalid or email is missing
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def decode_jwt_token(token: str) -> dict:
    """
    Decode a JWT token and return its payload as a dictionary.

    :param token: JWT access token
    :return: Dictionary with decoded token payload, or empty dict if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return {}
