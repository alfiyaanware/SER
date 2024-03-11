// Function to handle uploading audio files
function uploadFromFile() {
    const uploadInput = document.getElementById('uploadInput');
    const file = uploadInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('audio', file); // Ensure the field name matches the expected field name in the FastAPI endpoint

        fetch('/process_audio/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to process audio: ' + response.statusText);
            }
        })
        .then(data => {
            window.location.href = '/result/';
        })
        .catch(error => console.error('Error:', error));
    } else {
        console.error('No file selected.');
    }
}


// Function to start recording audio
function startRecording() {
    // Implement recording functionality here
}
