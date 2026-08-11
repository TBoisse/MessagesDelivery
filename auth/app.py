# extern imports
from fastapi import Depends, FastAPI, HTTPException, Response, Cookie, Request
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

@app.get("/verify")
def verify(access_token: str | None = Cookie(default=None)):
    if not access_token:
        return Response(status_code=401)
    _, code = decode_token(access_token)
    return Response(status_code=code)

@app.post("/login")
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    # TODO : look up async Session and db execute
    result = db.execute(
        select(User).where(User.username == request.username)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(str(request.username))

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=MAX_AGE,
    )
    return {"message" : "logged in"}

@app.post("/signin")
def signin(request: SigninRequest, response: Response, db: Session = Depends(get_db)):
    user = User(
        username=request.username,
        phone_number=request.phone_number,
        email=request.email,
    )

    message, code = save_to_db(db, user)
    if code != 200:
        raise HTTPException(
            status_code=code,
            detail=message
        )

    token = create_access_token(str(request.username))

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=MAX_AGE,
    )
    return {"message" : "signed in"}

@app.get("/admin/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User.username).all()

    return {
        "users": [
            user.username
            for user in users
        ]
    }