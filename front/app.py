from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request : Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/user/login")
async def login(request : Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@app.get("/user/signin")
async def signin(request : Request):
    return templates.TemplateResponse(
        request=request,
        name="signin.html"
    )