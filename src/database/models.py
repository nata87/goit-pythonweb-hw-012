from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.settings.config import Base
import enum


class Role(enum.Enum):
    admin: str = "admin"
    user: str = "user"


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)
    confirmed = Column(Boolean, default=False)
    contacts = relationship("Contact", back_populates="owner")

    roles = Column("roles", Enum(Role), default=Role.user)


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    additional_info = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="contacts")