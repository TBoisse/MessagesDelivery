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
from src.requests import CreateChatRequest, DeleteChatRequest
from src.tables import Chat, ChatMember, Message
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
    if chat.creator_id != user_id:
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
