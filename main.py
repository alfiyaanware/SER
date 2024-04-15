from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import numpy as np

from json_tricks import dump, load
from audio_model import test
from pydub import AudioSegment, effects
import librosa
import noisereduce as nr

import tensorflow as tf
import keras
import sklearn
from keras.models import model_from_json
from keras.models import load_model

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index1.html", {"request": request})


@app.get('/old', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("old.html", {"request": request})

@app.get('/about', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})



@app.post("/process_audio/")
async def process_audio(audio: UploadFile = File(...)):
    # Determine the directory where you want to save the uploaded files
    print("inside pa")
    save_directory = "audio_repository"

    # Create the directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    # Concatenate the directory path and the filename
    file_path = os.path.join(save_directory, audio.filename)

    # Save the uploaded file to the specified directory
    with open(file_path, "wb") as f:
        f.write(await audio.read())

    # Returning 'OK' status along with the file path
    return {"message": "Audio processed successfully.", "file_path": file_path}


@app.get("/result/", response_class=HTMLResponse)
async def show_result(request: Request):
    
    folder_path = os.path.join(os.getcwd(), 'audio_repository')

    output = test()
    return templates.TemplateResponse("result.html", {"request": request, "message": output, "path":folder_path})
