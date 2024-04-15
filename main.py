from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import numpy as np
from fastapi import FastAPI, Form, HTTPException
from resemble import Resemble
import requests

from json_tricks import dump, load
from audio_model import test
from pydub import AudioSegment, effects
import noisereduce as nr

import tensorflow as tf
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

Resemble.api_key('yarlRYrBdHh4OU7IpP1S3gtt')

@app.get("/tts")
async def read_index():
    with open("static/tts.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)
    
@app.post("/generate_audio")
async def generate_audio(sentence: str = Form(...)):
    try:
        # Get projects directly from response (assuming 'items' key holds projects)
        response = Resemble.v2.projects.all(1, 10)
        project_uuid = response['items'][0]['uuid']

        # Get your Voice uuid. In this example, we'll obtain the first.
        voice_uuid = Resemble.v2.voices.all(1, 10)['items'][0]['uuid']

        # Let's create a clip!
        body = sentence
        response = Resemble.v2.clips.create_sync(project_uuid, voice_uuid, body)
        print(response)

        # Check for successful clip creation
        if response.get('success') is True:
            clip_data = response.get('item')
            if clip_data:
                audio_url = clip_data['audio_src']

                # Download the audio using requests
                response = requests.get(audio_url)

                if response.status_code == 200:
                    # Return the audio content
                    return response.content
                else:
                    raise HTTPException(status_code=response.status_code, detail=f"Error downloading audio: {response.status_code}")
            else:
                raise HTTPException(status_code=500, detail="Error: No clip data found in response.")
        else:
            raise HTTPException(status_code=500, detail="Error creating clip. Check response for details.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))