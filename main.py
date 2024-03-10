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
    # Implement audio processing logic here
    # For example, you could save the audio file to a directory or perform some analysis

    # For demonstration, we'll just save the file to a directory
    file_path = os.path.join("audio_repository", "uploaded_audio.wav")
    with open(file_path, "wb") as f:
        f.write(await audio.read())

    # Returning 'OK' status
    return {"message": "Audio processed successfully."}

@app.get("/result/", response_class=HTMLResponse)
async def show_result(request: Request):
    # Implement logic to display results
    # For now, let's display a simple message
    return templates.TemplateResponse("result.html", {"request": request, "message": "Result will be displayed here."})
