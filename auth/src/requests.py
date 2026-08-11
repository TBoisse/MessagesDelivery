from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    phone_number: str

class SigninRequest(BaseModel):
    username: str
    phone_number: str
    email: str