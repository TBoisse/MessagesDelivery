# native imports
import os
import logging
logger = logging.getLogger(__name__)
# extern imports
from fastapi import Depends, FastAPI, HTTPException, Response, Request
from fastapi.security import HTTPBearer
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from hashids import Hashids
# intern imports
from src.requests import CreateChatRequest, DeleteChatRequest, CreateMessageRequest
from src.tables import User, Chat, ChatMember, Message
from src.database import get_db, save_to_db, delete_in_db

app = FastAPI()
security = HTTPBearer()

COOKIE_NAME = "access_token"
hashids = Hashids(
    salt=os.environ.get("MESSAGE_KEY"),
    min_length=14,
)

@app.get("/chat")
def get_chat(request : Request, db : Session = Depends(get_db)):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=401)

    chats = db.scalars(
        select(Chat)
        .join(ChatMember, ChatMember.chat_id == Chat.chat_id)
        .where(ChatMember.user_id == user_id)
    ).all()

    return [
        {
            "chat_id": hashids.encode(chat.chat_id),
            "chat_name": chat.chat_name,
            "description": chat.description,
            "icon": chat.icon,
        }
        for chat in chats
    ]


@app.post("/chat")
def create_chat(request : Request, create_request: CreateChatRequest, db: Session = Depends(get_db)):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=401)

    chat = Chat(
        chat_name=create_request.chat_name,
        description=create_request.description,
        icon=create_request.icon,
        creator_id=user_id
    )

    message, code = save_to_db(db, chat)
    if code != 200:
        raise HTTPException(
            status_code=code,
            detail=message
        )

    chat_member = ChatMember(
        chat_id=chat.chat_id,
        user_id=user_id
    )

    message, code = save_to_db(db, chat_member)
    if code != 200:
        raise HTTPException(
            status_code=code,
            detail=message
        )

    return {"message": f"Chat created"}, 200

@app.delete("/chat")
def delete_chat(request : Request, delete_request: DeleteChatRequest, db: Session = Depends(get_db)):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=401)

    chat_id = hashids.decode(delete_request.chat_id)
    if not chat_id:
        raise HTTPException(status_code=404)

    chat = db.scalar(select(Chat).where(Chat.chat_id == chat_id[0]))
    if not chat or chat.creator_id != user_id:
        raise HTTPException(status_code=403)

    try:
        db.execute(
            delete(ChatMember).where(ChatMember.chat_id == chat_id)
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500)

    message, code = delete_in_db(db, chat)
    if code != 200:
        raise HTTPException(
            status_code=code,
            detail=message
        )

    return {"message": f"Chat deleted"}, 200

@app.get("/message/{encoded_chat_id}")
def get_messages(request : Request, encoded_chat_id: str, db: Session = Depends(get_db)):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=401)
    decoded_chat_id = hashids.decode(encoded_chat_id)
    if not decoded_chat_id:
        raise HTTPException(status_code=404)
    chat_id = decoded_chat_id[0]
    chat = db.scalar(select(Chat).where(Chat.chat_id == chat_id))
    if not chat:
        raise HTTPException(status_code=403)

    members = db.execute(
        select(User.user_id, User.username)
        .join(ChatMember)
        .where(ChatMember.chat_id == chat_id)
    ).all()
    members_corresp = {
        m.user_id: m.username
        for m in members
    }

    messages = db.scalars(
        select(Message)
        .where(Message.conversation_id == chat_id)
        .order_by(Message.created_at)
    ).all()

    return [
        {
            "user": members_corresp[message.sender_id],
            "content": message.content,
            "hour": f"{message.created_at.hour}:{message.created_at.minute}",
            "is_user": message.sender_id == user_id,
        }
        for message in messages
    ]

@app.post("/message")
def create_message(request : Request, create_request: CreateMessageRequest, db: Session = Depends(get_db)):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=401)
    chat_id = hashids.decode(create_request.chat_id)
    if not chat_id:
        raise HTTPException(status_code=404)
    chat = db.scalar(select(Chat).where(Chat.chat_id == chat_id[0]))
    if not chat:
        raise HTTPException(status_code=403)

    message = Message(
        conversation_id=chat_id[0],
        sender_id=user_id,
        content=create_request.content
    )


    status, code = save_to_db(db, message)
    if code != 200:
        raise HTTPException(
            status_code=code,
            detail=status
        )

    return {"message": f"Message created"}, 200