# native imports
import json
# extern imports
from fastapi import Depends, FastAPI, HTTPException, Response, Request
from fastapi.security import HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
# intern imports
from src.requests import LoginRequest, SigninRequest
from src.tables import User
from src.token import decode_token, create_access_token, MAX_AGE
from src.database import get_db, save_to_db

app = FastAPI()
security = HTTPBearer()

COOKIE_NAME = "access_token"

# ############################
# USER
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
    user = db.scalar(
        select(User).where(User.phone_number == login_request.phone_number)
    )
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
    token = create_access_token(str(login_request.phone_number))
    access_tokens : list = json.loads(request.cookies.get(COOKIE_NAME, "[]"))
    phones_decoded = [
        0 if (decoded := decode_token(t))[1] != 200 else decoded[0]["sub"]
        for t in access_tokens
    ]
    if login_request.phone_number in phones_decoded:
        user_index = phones_decoded.index(login_request.phone_number)
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
    user = User(
        username=signin_request.username,
        phone_number=signin_request.phone_number,
        email=signin_request.email,
    )

    message, code = save_to_db(db, user)
    if code != 200:
        raise HTTPException(
            status_code=code,
            detail=message
        )

    token = create_access_token(str(signin_request.phone_number))
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
