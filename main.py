from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import numpy as np

from json_tricks import dump, load

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
    # Implement logic to display results
    total_length = 314818 
    frame_length = 2048
    hop_length = 512
    
    folder_path = os.path.join(os.getcwd(), 'audio_repository')

    for subdir, dir, files in os.walk(folder_path):
        for file in files:
            file_path=os.path.join(folder_path,file)
    
    print(file_path)

    _, sr = librosa.load(path = file_path, sr = None) # sr (the sample rate) is used for librosa's MFCCs. '_' is irrelevant.
    # Load the audio file.
    rawsound = AudioSegment.from_file(file_path)
    # Normalize the audio to +5.0 dBFS.
    normalizedsound = effects.normalize(rawsound, headroom = 0)
    # Transform the normalized audio to np.array of samples.
    normal_x = np.array(normalizedsound.get_array_of_samples(), dtype = 'float32')
    # Trim silence from the beginning and the end.
    xt, index = librosa.effects.trim(normal_x, top_db=30)
    # Pad for duration equalization.
    padded_x = np.pad(xt, (0, total_length-len(xt)), 'constant')
    # Noise reduction.
    final_x = nr.reduce_noise(padded_x, sr=sr) 

    f1 = librosa.feature.rms(y=final_x, frame_length=frame_length, hop_length=hop_length) # Energy - Root Mean Square
    f2 = librosa.feature.zero_crossing_rate(final_x , frame_length=frame_length, hop_length=hop_length, center=True) # ZCR
    f3 = librosa.feature.mfcc(y=final_x, sr=sr, n_mfcc=13, hop_length = hop_length) # MFCC
    rms = []
    zcr = []
    mfcc = []

    rms.append(f1)
    zcr.append(f2)
    mfcc.append(f3)

    f_rms = np.asarray(rms).astype('float32')
    f_rms = np.swapaxes(f_rms,1,2)
    f_zcr = np.asarray(zcr).astype('float32')
    f_zcr = np.swapaxes(f_zcr,1,2)
    f_mfccs = np.asarray(mfcc).astype('float32')
    f_mfccs = np.swapaxes(f_mfccs,1,2)

    print('ZCR shape:',f_zcr.shape)
    print('RMS shape:',f_rms.shape)
    print('MFCCs shape:',f_mfccs.shape)

    X = np.concatenate((f_zcr, f_rms, f_mfccs), axis=2)

    print(np.shape(X))

    saved_model_path = './model.json'
    saved_weights_path = './model_weights.h5'

    with open(saved_model_path , 'r') as json_file:
        json_savedModel = json_file.read()

    model = tf.keras.models.model_from_json(json_savedModel)
    model.load_weights(saved_weights_path)

    model.compile(loss='categorical_crossentropy',
                    optimizer='RMSProp',
                    metrics=['categorical_accuracy'])

    predictions = model.predict(X)
    y_pred_class = np.argmax(predictions, axis=1)
    pred=y_pred_class[0]
    print(predictions)
    print(pred)

    labels={0: 'happy', 1: 'happy', 2: 'sad', 3:'fear', 4:'fear', 5:'sad', 6: 'happy'}

    output=labels[pred]

    os.remove(file_path)
    # For now, let's display a simple message
    return templates.TemplateResponse("result.html", {"request": request, "message": output})
