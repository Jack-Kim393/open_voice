
# Technical Requirements Document (TRD) for Open Voice UI

## 1. System Architecture

The system will be composed of three main components:

*   **Frontend:** A web-based UI built with HTML, CSS, and JavaScript. This will be the main interface for the user to upload a tone color audio, an optional style reference audio, and input text.
*   **Backend:** A Python-based server using Flask. This server will handle requests from the frontend, interact with the OpenVoice model, and return the generated audio.
*   **OpenVoice Model:** The core voice cloning model from the OpenVoice project. The backend will use this model to perform the voice cloning, dynamically generating speaker embeddings from the user-provided audio files.
*   **Docker Container:** The entire application will be packaged in a Docker container for portability and easy deployment.

## 2. Technology Stack

*   **Programming Language:** Python 3.9+
*   **Web Framework:** Flask
*   **Frontend:** HTML5, CSS3, JavaScript
*   **Containerization:** Docker
*   **Voice Cloning Model:** OpenVoice

## 3. UI Design

The UI will be a single-page application with the following elements:

*   **Header:** A title for the application.
*   **File Upload Section:** Two `input` fields of type `file`:
    *   One for the mandatory Tone Color reference audio.
    *   One for the optional Style Reference audio.
    *   Each input will have descriptive text and an `accept` attribute for audio formats (e.g., `.wav, .mp3`).
*   **Text Input Section:** A `textarea` for the user to input text.
*   **Generate Button:** A `button` to start the voice cloning process.
*   **Progress Indicator:** A loading spinner element, initially hidden, to be displayed during processing.
*   **Result Section:** An `audio` element to play the generated audio and a `a` tag to download it.

## 4. Frontend Logic

*   **Form Submission:** On clicking the "Generate" button, a JavaScript function will:
    1.  Show the progress indicator and disable the button.
    2.  Create a `FormData` object.
    3.  Append the tone color file, the optional style reference file, and the input text to the `FormData`.
    4.  Send the data to the `/generate` endpoint using a `fetch` POST request.
*   **Response Handling:** Upon receiving a response:
    1.  Hide the progress indicator and re-enable the button.
    2.  If successful, update the `src` of the `audio` element with the returned file path and make the result section visible.
    3.  If an error occurs, display an alert to the user.

## 5. Backend API

The backend will expose the following API endpoint:

*   **`POST /generate`:**
    *   **Request (multipart/form-data):**
        *   `voice_file`: The uploaded tone color audio file (required).
        *   `style_file`: The uploaded style reference audio file (optional).
        *   `text`: The text to be spoken (required).
    *   **Response (JSON):**
        *   On success: `{"audio_file": "/outputs/generated_audio.wav"}`
        *   On failure: `{"error": "Error message"}`

## 6. Core Logic Implementation (`voice_cloner.py`)

*   The `clone_voice` function will be modified to accept an optional `style_reference_path`.
*   **If `style_reference_path` is provided:** The function will call `se_extractor.get_se` on this path to generate the `source_se` (the style embedding).
*   **If `style_reference_path` is NOT provided:** The function will load the default, neutral `source_se` from the `en_default_se.pth` file, maintaining the original behavior.
*   The `target_se` (the voice tone) will always be generated from the main `reference_speaker_path`.

## 7. Dockerization

*   **`Dockerfile`:** A `Dockerfile` will be created to build the Docker image.
    *   The base image will be a Python image (e.g., `python:3.9-slim`).
    *   It will copy the project files into the image.
    *   It will install the dependencies from `requirements.txt`.
    *   It will set the command to run the backend server.
*   **Multi-architecture Build:** The Docker image will be built for both `linux/amd64` and `linux/arm64` architectures using `docker buildx`.

## 8. Command File

A `run.sh` file will be provided to simplify the execution of the application. This file will contain the following commands:

```bash
#!/bin/bash
docker build -t open-voice-ui .
docker run -p 5000:5000 open-voice-ui
```
