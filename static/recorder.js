const recordBtn = document.getElementById('record-btn');
let recorder, mediaStream;

recordBtn.addEventListener('click', toggleRecording);

function toggleRecording() {
  if (recorder === undefined) {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(startRecording)
      .catch(handleError);
  } else {
    stopRecording();
  }
}

function startRecording(stream) {
  mediaStream = stream;
  recordBtn.textContent = 'Stop Recording';
  recorder = new MediaRecorder(stream);
  recorder.ondataavailable = handleData;
  recorder.start();
}

function stopRecording() {
  recorder.stop();
  recordBtn.textContent = 'Record Audio';
}

function handleData(event) {
  const audioBlob = new Blob([event.data], { type: 'audio/webm' });
  const url = window.URL.createObjectURL(audioBlob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'recording.webm';
  link.click();

  releaseResources();
}

function handleError(error) {
  console.error('Error:', error);
}

function releaseResources() {
  mediaStream.getTracks().forEach(track => track.stop());
  recorder = undefined;
  mediaStream = undefined;
}
