
# Task List for Open Voice UI Project

This document breaks down the development of the Open Voice UI project into smaller, manageable tasks. Each task includes detailed commands and code snippets to guide a junior developer through the process.

## Phase 1: Project Setup & Backend

### Task 1.1: Create Project Directory and Virtual Environment

**Goal:** Set up a clean and isolated environment for the project.

**Commands:**

```bash
# Create the main project directory
mkdir open-voice-ui
cd open-voice-ui

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### Task 1.2: Install Flask

**Goal:** Install the Flask web framework.

**Command:**

```bash
pip install Flask
```

### Task 1.3: Create Basic Flask Application Structure

**Goal:** Create the necessary folders and empty files for the Flask application.

**Commands:**

```bash
# Create folders for templates and static files
mkdir templates
mkdir static

# Create empty files
touch app.py
touch templates/index.html
touch static/style.css
touch static/script.js
touch requirements.txt
```

### Task 1.4: Create a "Hello World" Flask Server

**Goal:** Create a minimal Flask server to ensure the setup is working.

**File:** `app.py`

**Code:**

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**File:** `templates/index.html`

**Code:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open Voice UI</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Hello, World!</h1>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
```

**To Run:**

```bash
python app.py
```

Then, open a web browser and go to `http://127.0.0.1:5000`.

## Phase 2: OpenVoice Integration

### Task 2.1: Clone the OpenVoice Repository

**Goal:** Get the OpenVoice code.

**Command:**

```bash
git clone https://github.com/myshell-ai/OpenVoice.git
```

### Task 2.2: Install OpenVoice Dependencies

**Goal:** Install all the Python packages required by OpenVoice.

**Command:**

```bash
pip install -r OpenVoice/requirements.txt
```

### Task 2.3: Download OpenVoice Models

**Goal:** Download the pre-trained models required by OpenVoice.

**Instructions:**

Follow the instructions in the `OpenVoice` repository to download the models. You will likely need to create a `checkpoints` directory and place the model files there.

### Task 2.4: Create an OpenVoice Wrapper

**Goal:** Create a Python module that simplifies the interaction with the OpenVoice library.

**File:** `voice_cloner.py`

**Code (Simplified Example):**

```python
# This is a simplified example. You will need to adapt the code from the OpenVoice repository.
import se_extractor
from api import BaseSpeakerTTS, ToneColorConverter

def clone_voice(text, input_audio_path, output_audio_path):
    """
    Clones a voice from an audio file and generates speech from text.
    """
    # Load models
    base_speaker_tts = BaseSpeakerTTS()
    tone_color_converter = ToneColorConverter()

    # Extract speaker embedding
    target_se, audio_name = se_extractor.get_se(input_audio_path, tone_color_converter, 'en')

    # Generate speech
    base_speaker_tts.tts(text, target_se, output_audio_path)

    print(f"Generated audio saved to {output_audio_path}")

```

### Task 2.5: Integrate OpenVoice with Flask

**Goal:** Create an API endpoint in the Flask app to handle voice cloning requests.

**File:** `app.py`

**Code:**

```python
from flask import Flask, render_template, request, jsonify
import os
# from voice_cloner import clone_voice # You will import your wrapper here

app = Flask(__name__)

# ... (index route from before)

@app.route('/generate', methods=['POST'])
def generate():
    if 'voice_file' not in request.files:
        return jsonify({'error': 'No voice file provided'}), 400

    voice_file = request.files['voice_file']
    text = request.form.get('text')

    # Save the uploaded file
    # ... (code to save the file)

    # Call the voice cloning function
    # clone_voice(text, saved_file_path, output_audio_path)

    # Return the path to the generated audio
    # return jsonify({'audio_file': output_audio_path})
    return jsonify({'message': 'This is a placeholder response.'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Phase 3: Frontend Development

### Task 3.1: Design the HTML Structure

**Goal:** Create the user interface elements in the `index.html` file.

**File:** `templates/index.html`

**Code:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open Voice UI</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Open Voice UI</h1>
    <form id="voice-form">
        <div>
            <label for="voice_file">Upload Voice File:</label>
            <input type="file" id="voice_file" name="voice_file" accept="audio/*" required>
        </div>
        <div>
            <label for="text">Text to Speak:</label>
            <textarea id="text" name="text" rows="4" required></textarea>
        </div>
        <button type="submit">Generate</button>
    </form>
    <div id="result">
        <h2>Generated Audio</h2>
        <audio id="audio-player" controls></audio>
        <a id="download-link" download="generated_audio.wav">Download</a>
    </div>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
```

### Task 3.2: Style the UI

**Goal:** Add some basic styling to make the UI look clean.

**File:** `static/style.css`

**Code:**

```css
body {
    font-family: sans-serif;
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
}

form div {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input[type="file"], textarea {
    width: 100%;
    padding: 8px;
}

button {
    padding: 10px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
}

#result {
    margin-top: 20px;
}
```

### Task 3.3: Implement Frontend Logic

**Goal:** Write JavaScript to handle form submission and API interaction.

**File:** `static/script.js`

**Code:**

```javascript
document.getElementById('voice-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/generate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.audio_file) {
            const audioPlayer = document.getElementById('audio-player');
            const downloadLink = document.getElementById('download-link');

            audioPlayer.src = data.audio_file;
            downloadLink.href = data.audio_file;

            document.getElementById('result').style.display = 'block';
        } else {
            alert(data.error || 'An error occurred.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred.');
    });
});
```

## Phase 4: Dockerization & Deployment

### Task 4.1: Create a `Dockerfile`

**Goal:** Define the steps to create a Docker image for the application.

**File:** `Dockerfile`

**Code:**

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
```

### Task 4.2: Create a `.dockerignore` file

**Goal:** Exclude unnecessary files from the Docker image to keep it small.

**File:** `.dockerignore`

**Code:**

```
venv
.git
.idea
__pycache__
*.pyc
```

### Task 4.3: Freeze Dependencies

**Goal:** Create a `requirements.txt` file with all the project dependencies.

**Command:**

```bash
pip freeze > requirements.txt
```

### Task 4.4: Create a `run.sh` Script

**Goal:** Create a simple script to build and run the Docker container.

**File:** `run.sh`

**Code:**

```bash
#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t open-voice-ui .

# Run the Docker container
echo "Running Docker container..."
docker run -p 5000:5000 open-voice-ui
```

**To make it executable:**

```bash
chmod +x run.sh
```
