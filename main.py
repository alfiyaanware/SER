from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
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
from tts2 import speech_text
from transcript import transcribe

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    try:
        os.remove("static/synthesized_audio.wav")
    except Exception as e:
        print("reset audio file")
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

    output, result = test()
    
    return templates.TemplateResponse("result.html", {"request": request, "message": output, "path":folder_path, "text": result})

Resemble.api_key('yarlRYrBdHh4OU7IpP1S3gtt')

@app.get("/tts")
async def read_index():
    with open("static/tts.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)
    
@app.get("/tts2")
async def read_index():
    with open("static/tts2.html", "r") as f:
        
        return HTMLResponse(content=f.read(), status_code=200)
    
@app.post("/generate_audio_2")
async def read_index(sentence: str = Form(...), emotion: str = Form(...), voice: str = Form(...)):
    try:
        # os.remove("static/synthesized_audio.wav")
        if voice == 'male':
            voice_gender = 'en-US-DavisNeural	'  # Index for male voice
        elif voice == 'female':
            voice_gender = 'en-US-AriaNeural'  # Index for female voice
        
        print("inside main")
        speech_text(emotion, sentence, voice_gender)

        # if emotion == 'male':
        #     voice_index = 'en-US-DavisNeural	'  # Index for male voice
        # elif voice == 'female':
        #     voice_index = 'en-US-AriaNeural'  # Index for female voice

        return HTMLResponse(content=f"""
                    <script>
                        // Redirect to the audio URL
                        window.location.href = '/tts2';
                        // After 3 seconds, redirect back to the front page
                    </script>
                """, status_code=200)
    
    except Exception as e:
    # Handle exceptions here
        print("Exception occurred:", e)
        # Return an error response or redirect to an error page
        # For example:
        return RedirectResponse(url="/error")
    

    
@app.post("/generate_audio")
async def generate_audio(sentence: str = Form(...), voice: str = Form(...)):
    try:
        # Get projects directly from response (assuming 'items' key holds projects)
        response = Resemble.v2.projects.all(1, 10)
        project_uuid = response['items'][0]['uuid']

        # Get your Voice uuid based on the selected voice
        if voice == 'male':
            voice_index = 1  # Index for male voice
        elif voice == 'female':
            voice_index = 2  # Index for female voice

        # Get your Voice uuid. In this example, we'll obtain the first.
        voice_uuid = Resemble.v2.voices.all(1, 10)['items'][voice_index]['uuid']

        # Let's create a clip!
        body = sentence
        response = Resemble.v2.clips.create_sync(project_uuid, voice_uuid, body)
        print("Response: ", response)


        # Check for successful clip creation
        if response.get('success') is True:
            clip_data = response.get('item')

            if clip_data:
                audio_url = clip_data['audio_src']
                print(audio_url)

                # # Download the audio using requests
                # response = requests.get(audio_url)
                # print("response content", response.content)
                # return RedirectResponse(url=audio_url)
                return HTMLResponse(content=f"""
                    <script>
                        // Redirect to the audio URL
                        window.location.href = '{audio_url}';
                        // After 3 seconds, redirect back to the front page
                        setTimeout(function() {{
                            window.location.href = '/';
                        }}, 7000); // 3000 milliseconds = 3 seconds
                    </script>
                """, status_code=200)
                # return templates.TemplateResponse("/static/tts.html", {"audio_url": audio_url})


    except Exception as e:
        # Handle exceptions here
        print("Exception occurred:", e)
        # Return an error response or redirect to an error page
        # For example:
        return RedirectResponse(url="/error")