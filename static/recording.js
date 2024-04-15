const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');
const playButton = document.getElementById('play');
const submitButton = document.getElementById('submit');
const output = document.getElementById('output');
let audioRecorder;
let audioChunks = [];

navigator.mediaDevices.getUserMedia({ audio: true })
.then(stream => {
    audioRecorder = new MediaRecorder(stream);
    audioRecorder.addEventListener('dataavailable', e => {
        audioChunks.push(e.data);
    });

    startButton.addEventListener('click', () => {
        audioChunks = [];
        audioRecorder.start();
        output.innerHTML = 'Recording started! Speak now.';
    });

    stopButton.addEventListener('click', () => {
        audioRecorder.stop();
        output.innerHTML = 'Recording stopped! Click on the play button to play the recorded audio.';
    });

    playButton.addEventListener('click', () => {
        const blobObj = new Blob(audioChunks, { type: 'audio/webm' });
        const audioUrl = URL.createObjectURL(blobObj);
        const audio = new Audio(audioUrl);
        audio.play();
        output.innerHTML = 'Playing the recorded audio!';
    });

    submitButton.addEventListener('click', () => {
    const blobObj = new Blob(audioChunks, { type: 'audio/webm' });
    console.log("Blob created:", blobObj);

    const formData = new FormData();
    formData.append('audio', blobObj);
    console.log("FormData created:", formData);

    fetch('/process_audio', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log("Response received:", response);
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        console.log("Response data:", data);
        output.innerHTML = 'Audio submitted for processing!';
        if(data){
            window.location.href = '/result/';
        }
    })
    .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
        output.innerHTML = 'Error submitting audio for processing.';
    });
});
    

}).catch(err => {
    console.log('Error: ' + err);
});