// Function to handle uploading audio files
function uploadFromFile() {
    const uploadInput = document.getElementById('uploadInput');
    const file = uploadInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/process_audio/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/result/';
            } else {
                console.error('Error:', response.statusText);
            }
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
