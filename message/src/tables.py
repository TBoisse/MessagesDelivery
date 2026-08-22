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

class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True, index=True)
    chat_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(500), nullable=True)
    creator_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )
    created_at = Column(
        DateTime,
        default=lambda : datetime.now(timezone.utc),
        nullable=False,
    )

class ChatMember(Base):
    __tablename__ = "chat_members"

    chat_id = Column(
        Integer,
        ForeignKey("chats.chat_id"),
        primary_key=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        primary_key=True,
    )

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(
        Integer,
        ForeignKey("chats.chat_id"),
        nullable=False,
    )

    sender_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False,
    )

    content = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda : datetime.now(timezone.utc),
        nullable=False,
    )
