"""
This module represents the front endpoints.
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request : Request):
    """
    Front index page.
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/user/login")
async def login(request : Request):
    """
    Login page.
    """
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@app.get("/user/signin")
async def signin(request : Request):
    """
    Signin page.
    """
    return templates.TemplateResponse(
        request=request,
        name="signin.html"
    )
