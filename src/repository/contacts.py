from sqlalchemy.orm import Session
from ..database.models import Contact
from ..schemas.contacts import ContactCreate, ContactUpdate
from datetime import datetime, timedelta
from src.database.models import User

def get_contacts(db: Session, user_id: int):
    """
    Retrieve all contacts for a specific user.

    :param db: Database session
    :param user_id: ID of the user
    :return: List of Contact objects
    """
    return db.query(Contact).filter(Contact.user_id == user_id).all()

def create_contact(db: Session, contact: ContactCreate, user_id: int):
    """
    Create a new contact for the user.

    :param db: Database session
    :param contact: Contact creation data
    :param user_id: ID of the user
    :return: Created Contact object
    """
    db_contact = Contact(**contact.dict(), user_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contact(db: Session, contact_id: int, user_id: int):
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user_id).first()

def update_contact(db: Session, contact_id: int, contact: ContactUpdate, user_id: int):
    """
    Update an existing contact.

    :param db: Database session
    :param contact_id: ID of the contact to update
    :param contact: Updated contact data
    :param user_id: ID of the user
    :return: Updated Contact object or None
    """
    db_contact = get_contact(db, contact_id, user_id)
    if db_contact:
        for field, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int, user_id: int):
    """
    Delete a contact by ID if it belongs to the specified user.

    :param db: SQLAlchemy session object
    :param contact_id: ID of the contact to delete
    :param user_id: ID of the user (used for ownership check)
    :return: The deleted Contact object if found, else None
    """
    db_contact = get_contact(db, contact_id, user_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts(db: Session, query: str, user_id: int):
    """
    Search for contacts by first name, last name, or email.

    :param db: Database session
    :param query: Search term
    :param user_id: ID of the user
    :return: List of matching Contact objects
    """
    return db.query(Contact).filter(
        Contact.user_id == user_id,
        (Contact.first_name.ilike(f"%{query}%")) |
        (Contact.last_name.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%"))
    ).all()

def get_upcoming_birthdays(db: Session, user_id: int):
    """
    Retrieve contacts with upcoming birthdays within the next 7 days.

    :param db: SQLAlchemy session object
    :param user_id: ID of the user whose contacts to filter
    :return: List of Contact objects with birthdays in the next 7 days
    """
    today = datetime.today().date()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(
        Contact.user_id == user_id,
        Contact.birthday.between(today, next_week)
    ).all()

def confirm_email(email: str, db: Session) -> None:
    """
    Confirm a user's email address by setting their status to verified.

    :param email: Email address to confirm
    :param db: SQLAlchemy session object
    :return: None
    """
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.is_verified = True
        db.commit()
