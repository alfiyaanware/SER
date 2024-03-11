from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index1.html", {"request": request})

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
    # Implement logic to display results
    total_length = 314818 
    frame_length = 2048
    hop_length = 512
    
    folder_path = 'C:/Users/Alfiya Anware/Desktop/github/SER/audio_repository'

    for subdir, dir, file in os.walk(folder_path):
        for i in file:
            print(os.path.join(subdir,i))
    
    file = '1001_ITS_NEU_XX.wav'
    # For now, let's display a simple message
    return templates.TemplateResponse("result.html", {"request": request, "message": "Result will be displayed here."})
