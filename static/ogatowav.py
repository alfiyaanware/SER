from pydub import AudioSegment
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

def convert_to_wav(oga_data):
  # Convert Blob data to byte array
  audio_data = oga_data.read()

  # Decode OGA data (using pydub library)
  oga_audio = AudioSegment.from_ogg(audio_data)

  # Convert to WAV format
  wav_audio = oga_audio.export(format="wav")

  # Save as WAV file
  with open("uploads/recording.wav", "wb") as wav_file:
    wav_file.write(wav_audio)

  return "Success"  # Or appropriate response

# Handle POST request from frontend
def handle_audio(request):
    if request.method == 'POST':
        oga_blob = request.FILES['oga_file']
        response = convert_to_wav(oga_blob)
        return JSONResponse({'message': response})
    else:
        return HTTPException()
