from pydantic import BaseModel

class LoginRequest(BaseModel):
    phone_number: str
    password: str

class SigninRequest(BaseModel):
    username: str
    phone_number: str
    password: str
