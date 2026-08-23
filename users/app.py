# native imports
import os
import logging
logger = logging.getLogger(__name__)
from datetime import timedelta
# extern imports
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPBearer
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from hashids import Hashids
from minio import Minio, error
# internal imports
from src.tables import User, Contact
from src.database import get_db, save_to_db, delete_in_db

# fast api
app = FastAPI()
security = HTTPBearer()
# hash func
hashids = Hashids(
    salt=os.environ.get("USERS_KEY"),
    min_length=14,
)
# minio
minio_client = Minio(
    "minio:9000",
    access_key=os.environ.get("MINIO_USER"),
    secret_key=os.environ.get("MINIO_PWD"),
    secure=False,
)
USERS_BUCKET = "users"
BASE_MINIO_URL = os.environ.get("BASE_MINIO_URL")

def get_object_name(object_type : str, user_id : str, object_name : str):
    return f"{object_type}/{user_id}/{object_name}"

def get_url_icon(object_type : str, user_id : str, object_name : str):
    return f"{BASE_MINIO_URL}/{USERS_BUCKET}/{get_object_name(object_type, user_id, object_name)}"

@app.get("/me")
def get_me(request : Request, db : Session = Depends(get_db)):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=401)
    user = db.scalar(
        select(User).where(User.user_id == user_id)
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    contacts = db.scalars(
        select(User)
        .join(Contact, User.user_id == Contact.contact_id)
        .where(Contact.user_id == user_id)
    )
    return {
        "username" : user.username,
        "phone_number" : user.phone_number,
        "url" : get_url_icon("icons", hashids.encode(user.user_id), "icons.png"),
        "contacts" : [
            {
                "username" : contact.username,
                "url" : get_url_icon("icons", hashids.encode(contact.user_id), "icons.png")
            } 
            for contact in contacts
        ]
    }

@app.get("/me/icon")
def get_icon(request : Request):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=401)
    return {"url" : get_url_icon("icons", hashids.encode(user_id), "icons.png")}

@app.put("/me/icon")
def put_icon(request : Request):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=401)
    object_name = get_object_name("icons", hashids.encode(user_id), "icons.png")
    presigned_url = minio_client.presigned_put_object(
        bucket_name=USERS_BUCKET,
        object_name=object_name,
        expires=timedelta(minutes=1),
    )
    return {"url" : presigned_url}