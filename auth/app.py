# extern imports
from fastapi import Depends, FastAPI, HTTPException, Response, Cookie
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# intern imports
from src.requests import LoginRequest, SigninRequest
from src.token import decode_token, create_access_token, MAX_AGE

app = FastAPI()
security = HTTPBearer()

@app.get("/verify")
def verify(access_token: str | None = Cookie(default=None)):
    if not access_token:
        return Response(status_code=401)
    _, code = decode_token(access_token)
    return Response(status_code=code)

@app.post("/login")
def login(request: LoginRequest, response: Response):
    if not request.username == "tmp":
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