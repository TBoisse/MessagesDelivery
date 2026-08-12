# native imports
import json
# extern imports
from fastapi import Depends, FastAPI, HTTPException, Response, Request
from fastapi.security import HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
# intern imports
from src.requests import CreateChatRequest
from src.tables import Chat, ChatMember, Message
from src.database import get_db, save_to_db

app = FastAPI()
security = HTTPBearer()

COOKIE_NAME = "access_token"

@app.get("/chat")
def get_chat(request : Request, db : Session = Depends(get_db)):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=403)

    chats = db.scalars(
        select(Chat)
        .join(ChatMember, ChatMember.chat_id == Chat.chat_id)
        .where(ChatMember.user_id == user_id)
    ).all()

    return [
        {
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
        raise HTTPException(status_code=403)

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