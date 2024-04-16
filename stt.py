import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "f738a8e88bf94704b8ef65645af93a7d"

# URL of the file to transcribe
FILE_URL = "/home/ap/Downloads/1001_ITS_SAD_XX.wav"

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    print(transcript.text)
