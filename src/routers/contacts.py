from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.repository import contacts as crud
from src.auth.dependencies import get_current_user
from src.settings.config import get_db
from src.database.models import Contact, User
from src.schemas.contacts import ContactCreate, ContactUpdate, ContactResponse

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get("/", response_model=List[ContactResponse])
def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_contacts(db, user_id=current_user.id)

@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_contact(db, contact, user_id=current_user.id)

@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_contact(db, contact_id, user_id=current_user.id)

@router.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(...).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    ...
    db.commit()
    db.refresh(contact)
    return contact 

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.delete_contact(db, contact_id, user_id=current_user.id)

@router.get("/search/")
def search_contacts(query: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.search_contacts(db, query, user_id=current_user.id)

@router.get("/birthdays/upcoming")
def upcoming_birthdays(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_upcoming_birthdays(db, user_id=current_user.id)
