import os
import azure.cognitiveservices.speech as speechsdk
import base64

# Replace 'YOUR_SUBSCRIPTION_KEY' and 'YOUR_SPEECH_REGION' with your actual values
def speech_text(emotion, text, speaker):
    print("inside st")
    os.environ['SPEECH_KEY'] = 'ddc91c1840ec4d2183bb20efe1a5fa65'
    os.environ['SPEECH_REGION'] = 'southeastasia'

    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

    # Use PullAudioOutputStream for audio data
    audio_output = speechsdk.audio.PullAudioOutputStream()

    # *Important:* While the chosen voice claims emotion support, it might not work as expected.
    speech_config.speech_synthesis_voice_name = speaker # Adjust if using a different voice

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

    # Get text from the console and synthesize to the default speaker.
    # print("Enter some text that you want to speak >")
    # text = input()

    # Emotion selection for informational purposes only (optional)
    # print("Enter the desired emotion (neutral, happy, sad, shouting, etc.):")
    # emotion = input().lower()  # Convert to lowercase for easier comparison

    # Construct SSML text with emotion styles
    ssml_text = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="{speech_config.speech_synthesis_voice_name}">
        <mstts:express-as style="{emotion}" styledegree="2">
        {text}
        </mstts:express-as>
    </voice>
    </speak>
    """

    # Synthesize speech and get audio data
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Get the audio data from the result
        audio_data = speech_synthesis_result.audio_data
        if audio_data:
            # Save audio data to a file
            with open('synthesized_audio.wav', 'wb') as audio_file:
                audio_file.write(audio_data)
            
            os.rename("synthesized_audio.wav", "static/synthesized_audio.wav")
            print("Speech synthesized and saved to 'synthesized_audio.wav'")
        else:
            print("Failed to retrieve synthesized audio data.")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    else:
        # Handle other potential reasons for cancellation (optional)
        pass
