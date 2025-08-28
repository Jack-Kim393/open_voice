
document.getElementById('voice-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = this;
    const formData = new FormData(form);
    const generateBtn = document.getElementById('generate-btn');
    const loader = document.getElementById('loader');
    const resultDiv = document.getElementById('result');

    // Show loader and disable button
    loader.style.display = 'block';
    generateBtn.disabled = true;
    resultDiv.style.display = 'none';

    fetch('/generate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.audio_file) {
            const audioPlayer = document.getElementById('audio-player');
            const downloadLink = document.getElementById('download-link');

            // Use a cache-busting query parameter to ensure the browser fetches the new file
            const audioUrl = data.audio_file + '?t=' + new Date().getTime();

            audioPlayer.src = audioUrl;
            downloadLink.href = audioUrl;

            resultDiv.style.display = 'block';
        } else {
            alert(data.error || 'An error occurred.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred.');
    })
    .finally(() => {
        // Hide loader and re-enable button
        loader.style.display = 'none';
        generateBtn.disabled = false;
    });
});
