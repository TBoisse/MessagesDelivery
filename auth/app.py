# native imports
import json
import os
from contextlib import asynccontextmanager
from datetime import timedelta
# extern imports
from fastapi import Depends, FastAPI, HTTPException, Response, Request
from fastapi.security import HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
import phonenumbers
from hashids import Hashids
from minio import Minio, error
# intern imports
from src.requests import LoginRequest, SigninRequest
from src.tables import User, Contact
from src.token import decode_token, create_access_token, MAX_AGE
from src.database import get_db, save_to_db

COOKIE_NAME = "access_token"
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
minio_public = Minio(
    "s3.localhost",
    access_key=os.environ.get("MINIO_USER"),
    secret_key=os.environ.get("MINIO_PWD"),
    secure=False,
)
USERS_BUCKET = "users"
DEFAULT_ICON_URL = "icon/default/default.png"

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not minio_client.bucket_exists(USERS_BUCKET):
        minio_client.make_bucket(USERS_BUCKET)
    try:
        minio_client.stat_object(
            USERS_BUCKET,
            DEFAULT_ICON_URL,
        )
    except Exception:
        minio_client.fput_object(
            bucket_name=USERS_BUCKET,
            object_name=DEFAULT_ICON_URL,
            file_path=str("data/default.png"),
            content_type="image/png",
        )
    yield
app = FastAPI(lifespan=lifespan)
security = HTTPBearer()

# ############################
# UTILS
# ############################

def get_object_name(object_type : str, user_id : str, object_name : str):
    return f"{object_type}/{user_id}/{object_name}"

def get_url_from_object(object_name : str):
    return minio_public.presigned_get_object(
        bucket_name=USERS_BUCKET,
        object_name=object_name,
        expires=timedelta(minutes=15),
    )

def parse_phone_number(phone_number):
    try:
        if phone_number[0] == "+":
            return phonenumbers.parse(phone_number, None)
        else:
            return phonenumbers.parse(phone_number, "FR")
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid phone number.",
        )

def database_phone(format_phone_number : phonenumbers.PhoneNumber):
    return f"+{format_phone_number.country_code}{format_phone_number.national_number}"

# ############################
# CONNEXION
# ############################

@app.post("/login")
def login(
    request : Request,
    login_request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
    ):
    # TODO : look up async Session and db execute
    #! Direct Cookie class can be passed instead of request
    format_phone_number = parse_phone_number(login_request.phone_number)
    db_phone = database_phone(format_phone_number)
    user = db.scalar(
        select(User).where(User.phone_number == db_phone)
    )
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
    if not check_password_hash(user.password_hash, login_request.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
    token = create_access_token(str(user.phone_number))
    access_tokens : list = json.loads(request.cookies.get(COOKIE_NAME, "[]"))
    phones_decoded = [
        0 if (decoded := decode_token(t))[1] != 200 else decoded[0]["sub"]
        for t in access_tokens
    ]
    if user.phone_number in phones_decoded:
        user_index = phones_decoded.index(user.phone_number)
        access_tokens[user_index] = token # mainly reset the expired date
    else:
        access_tokens.append(token)
        user_index = len(access_tokens) - 1
    response.set_cookie(
        key=COOKIE_NAME,
        value=json.dumps(access_tokens),
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=MAX_AGE,
    )
    return {"user_index" : user_index}

@app.post("/signin")
def signin(
    request : Request,
    signin_request: SigninRequest,
    response: Response,
    db: Session = Depends(get_db)
    ):
    if len(signin_request.password) < 8:
        raise HTTPException(
            status_code=401,
            detail="Password length < 8 caracters",
        )
    format_phone_number = parse_phone_number(signin_request.phone_number)
    if not phonenumbers.is_possible_number(format_phone_number):
        raise HTTPException(
            status_code=401,
            detail="Invalid phone number.",
        )
    user = User(
        username=signin_request.username,
        phone_number=database_phone(format_phone_number),
        password_hash=generate_password_hash(signin_request.password),
        icon_url = None
    )
    message, code = save_to_db(db, user)
    if code != 200:
        raise HTTPException(
            status_code=code,
            detail=message
        )

    token = create_access_token(str(user.phone_number))
    access_tokens : list = json.loads(request.cookies.get(COOKIE_NAME, "[]"))
    access_tokens.append(token)
    user_index = len(access_tokens) - 1

    response.set_cookie(
        key=COOKIE_NAME,
        value=json.dumps(access_tokens),
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=MAX_AGE,
    )
    return {"user_index" : user_index}

# ############################
# USERS
# ############################

@app.get("/me/user")
def get_me(request : Request, db : Session = Depends(get_db)):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=409, detail="Issue happened internaly.")
    user = db.scalar(
        select(User).where(User.user_id == user_id)
    )
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    contacts = db.scalars(
        select(User)
        .join(Contact, User.user_id == Contact.contact_id)
        .where(Contact.user_id == user_id)
    )
    return {
        "username" : user.username,
        "phone_number" : user.phone_number,
        "url" : get_url_from_object(user.icon_url if user.icon_url else DEFAULT_ICON_URL),
        "contacts" : [
            {
                "username" : contact.username,
                "user_id" : hashids.encode(contact.user_id),
                "url" : get_url_from_object(contact.icon_url if contact.icon_url else DEFAULT_ICON_URL)
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
    return {"url" : ""}

@app.put("/me/icon")
def put_icon(request : Request):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=401)
    object_name = get_object_name("icons", hashids.encode(user_id), "icons.png")
    presigned_url = minio_public.presigned_put_object(
        bucket_name=USERS_BUCKET,
        object_name=object_name,
        expires=timedelta(minutes=1),
    )
    return {"url" : presigned_url}

# ############################
# ADMIN
# ############################

@app.get("/admin/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User.username).all()

    return {
        "users": [
            user.username
            for user in users
        ]
    }

# ############################
# VERIFY
# ############################

@app.get("/verify")
def verify(request: Request):
    user_index = request.headers.get("X-User-Index")
    try:
        user_index = int(user_index)
    except Exception:
        return Response(status_code=401)
    access_tokens : list = json.loads(request.cookies.get(COOKIE_NAME, "[]"))
    if not access_tokens:
        return Response(status_code=401)
    _, code = decode_token(access_tokens[user_index])
    return Response(status_code=code)

@app.get("/verify/hard")
def verify_hard(request: Request, db: Session = Depends(get_db)):
    user_index = request.headers.get("X-User-Index")
    try:
        user_index = int(user_index)
    except Exception:
        return Response(status_code=401)
    access_tokens : list = json.loads(request.cookies.get(COOKIE_NAME, "[]"))
    if not access_tokens:
        return Response(status_code=401)
    payload, code = decode_token(access_tokens[user_index])
    if code != 200:
        return Response(status_code=code)
    user = db.scalar(
        select(User).where(User.phone_number == payload["sub"])
    )
    if user is None:
        return Response(status_code=401)
    return Response(
        status_code=200,
        headers={
            "X-User-Id": str(user.user_id),
        }
    )
