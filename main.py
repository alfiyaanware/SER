from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app= FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    context={'request': request}
    return templates.TemplateResponse("index.html", context)

@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    context={'request': request}
    return templates.TemplateResponse("index1.html", context)