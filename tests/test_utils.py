import pytest
from unittest.mock import patch
from src.auth import jwt
from src.auth.jwt import ALGORITHM, SECRET_KEY, create_access_token 
from src.services.auth import get_email_from_token
from src.auth.security import hash_password, verify_password
from src.auth.jwt import create_access_token
from jose import jwt  # <-- AGGIUNGI QUESTA RIGA


def test_create_access_token_decodes_correctly():
    email = "mock@example.com"
    token = create_access_token({"sub": email}, expires_minutes=5)
    result = get_email_from_token(token)
    assert result == email

def test_create_access_token_expired():
    """Перевірка простроченого токена (штучно змінений exp)."""
    email = "expired@example.com"
    payload = {"sub": email, "exp": 0}  # Unix epoch (прострочений)
    expired_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(Exception):
        _ = get_email_from_token(expired_token)

def test_hash_password_and_verify_password():
    password = "strongpassword"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)

def test_hash_password_is_different_each_time():
    """Перевіряє, що хеш кожного разу різний для одного і того ж паролю."""
    password = "test123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    assert hash1 != hash2