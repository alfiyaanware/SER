import assemblyai as aai

def transcribe(file_path):
    # Replace with your API key
    aai.settings.api_key = "f738a8e88bf94704b8ef65645af93a7d"

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)

    if transcript.status == aai.TranscriptStatus.error:
        e=transcript.error
    else:
        result=transcript.text

    return result