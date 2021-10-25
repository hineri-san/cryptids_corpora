from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from fastapi_app import crud, models, schemas
from fastapi_app.helper import *
# from fastapi_app.processing import project_to_fastlane

texts = download_texts()

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def project_send_get(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request, 'result': ''})


@app.post("/")
def project_unlock_post(request: Request, action: str = Form(...)):

    result = search(texts, action)
    return templates.TemplateResponse('index.html', context={'request': request, 'result': result})
