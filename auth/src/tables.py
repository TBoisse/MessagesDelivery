from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    phone_number = Column(String(30), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    icon_url = Column(String(255), nullable=True)

class Contact(Base):
    __tablename__ = "contacts"

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        primary_key=True,
    )

    contact_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        primary_key=True,
    )