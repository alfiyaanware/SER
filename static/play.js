const audioElement = document.getElementById('audio-player');

function playAudio() {
  audioElement.src = 'http://localhost:8000/synthesized_audio.wav'; // Adjust port if needed
  audioElement.load();
  audioElement.play();
}

playAudio(); // Call the function to play audio on page load
