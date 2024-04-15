import requests  # Import for downloading audio

from resemble import Resemble

Resemble.api_key('yarlRYrBdHh4OU7IpP1S3gtt')

# Get projects directly from response (assuming 'items' key holds projects)
response = Resemble.v2.projects.all(1, 10)
print(response)  # Optional: To inspect the entire response

project_uuid = response['items'][0]['uuid']
print(f"Project UUID: {project_uuid}")

# Get your Voice uuid. In this example, we'll obtain the first.
voice_uuid = Resemble.v2.voices.all(1, 10)['items'][0]['uuid']
print(f"Voice UUID: {voice_uuid}")

# Let's create a clip!
body = 'Chicken noodle soup with a soda'
response = Resemble.v2.clips.create_sync(project_uuid, voice_uuid, body)

# Check for successful clip creation
if response.get('success') is True:
    clip_data = response.get('item')
    if clip_data:
        audio_url = clip_data['audio_src']
        print(f"Audio source URL: {audio_url}")

        # Download the audio using requests
        response = requests.get(audio_url)

        if response.status_code == 200:
            with open('clip.wav', 'wb') as f:  # Adjust filename and format as needed
                f.write(response.content)
            print("Audio downloaded successfully!")
        else:
            print(f"Error downloading audio: {response.status_code}")
    else:
        print("Error: No clip data found in response.")
else:
    print("Error creating clip. Check response for details.")