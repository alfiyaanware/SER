import requests
import json

url = "https://typecast.ai/api/speak"

payload = json.dumps({
  "actor_id": "61de29b665ffbaa1cbe5ca23",
  "text": "hello i am alekya",
  "lang": "auto",
  "tempo": 1,
  "volume": 100,
  "pitch": 0,
  "xapi_hd": True,
  "max_seconds": 60,
  "model_version": "latest",
  "xapi_audio_format": "wav",
  "emotion_tone_preset": "happy-1"
})
headers = {
  'Content-Type': 'application/json', 
  'Authorization': 'Bearer __plt4H3kYxbDdzB4CuabGWdNSjQ24q27Qpmnz9wJAtnT'
}

response = requests.request("POST", url, headers=headers, data=payload)

speak_url = response.json()["result"]["speak_url"]

response_1 = requests.request("GET", speak_url, headers=headers, data=payload)

print(response_1.text)
print(response.text)

speech_data = requests.get(speak_url)

# Check for successful download
if speech_data.status_code == 200:
  # Save the speech data to a file (replace "output.wav" with your desired filename)
  with open("output.wav", "wb") as f:
    f.write(speech_data.content)
  print("Speech downloaded successfully!")
else:
  print(f"Error downloading speech. Status code: {speech_data.status_code}")

      # Import the Typecast SDK for your language (replace with actual import statement)
# from typecast import TypecastClient

# # Initialize the Typecast client with your API token
# client = TypecastClient(api_token="61de29b665ffbaa1cbe5ca23")

# # Text for speech generation
# text = "hello i am alekya"

# # Voice and emotion preferences
# actor_id = "61de29b665ffbaa1cbe5ca23"
# emotion_tone_preset = "happy-1"
# # ... other voice options (language, tempo, volume, etc.)

# # Generate speech using the SDK
# speech_data = client.generate_speech(
#     text=text,
#     actor_id=actor_id,
#     emotion_tone_preset=emotion_tone_preset,
#     # ... other options
# )

# # Download the speech data (method might vary depending on the SDK)
# downloaded_file = speech_data.download("output.wav") 

# if downloaded_file:
#   print("Speech downloaded successfully!")
# else:
#   print("Error downloading speech.")
