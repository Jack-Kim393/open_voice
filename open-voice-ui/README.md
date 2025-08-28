
# Open Voice UI

This project provides a user-friendly web interface for the [OpenVoice](https://github.com/myshell-ai/OpenVoice) text-to-speech and voice cloning library. It allows users to easily upload an audio file for voice tone, optionally provide another for speaking style, input text, and generate a natural-sounding voice clone.

## Features

- **Simple Web Interface:** No command-line knowledge needed. A clean UI for all interactions.
- **Style Control:** Use a separate audio file as a "Style Reference" to control the emotion, pace, and rhythm of the generated speech, resulting in more natural and less robotic voices.
- **User-Friendly Feedback:** The UI provides clear instructions, accepted file formats, and a loading indicator during processing to improve user experience.
- **One-Click Start (macOS):** A `start.command` script is provided for macOS users to launch the application with a single double-click, with no manual setup required.
- **Dockerized Environment:** For other platforms, all dependencies are managed within a Docker container, ensuring a consistent and easy setup process.

## Project Structure

```
open-voice-ui/
├── Dockerfile
├── OpenVoice/          # Cloned OpenVoice repository
├── app.py              # Flask web server
├── requirements.txt    # Python dependencies
├── run.sh              # Build and run script for Docker
├── start.command       # One-click start script for macOS
├── static/               # CSS and JavaScript files
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html      # Web UI template
├── uploads/            # Directory for user-uploaded audio
├── outputs/            # Directory for generated audio
└── voice_cloner.py     # Wrapper for OpenVoice library
```

## How to Run

### For macOS Users (Recommended)

Simply double-click the `start.command` file in the project's root directory. This will open a terminal window and automatically start the web server.

*Note: You may need to give the file execute permissions first. Run this command in your terminal once: `chmod +x start.command`*

### For Other Systems (using Docker)

**Prerequisites:**

- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

**Steps:**

1.  **Clone this repository.**
2.  **Download OpenVoice Models:** Ensure you have downloaded the pre-trained models as per the [OpenVoice repository](https://github.com/myshell-ai/OpenVoice) instructions and placed them in the `open-voice-ui/OpenVoice/checkpoints` directory.
3.  **Run the script:**
    ```bash
    ./run.sh
    ```

After starting the server using either method, access the web interface by opening your browser and navigating to `http://127.0.0.1:5000`.

## How to Use

1.  **Upload Voice for Tone Color:** Click the first "Choose File" button to select a short (3-10 seconds) audio file (`.wav`, `.mp3`) of the voice you want to clone.
2.  **(Optional) Upload Voice for Style:** Click the second "Choose File" button to select an audio file with the speaking style (emotion, pace) you want to imitate.
3.  **Enter Text:** In the text area, type the text you want the cloned voice to speak.
4.  **Generate:** Click the "Generate" button. A spinner will appear while the voice is being generated.
5.  **Listen and Download:** After a few moments, an audio player will appear with the generated speech. You can listen to it directly or download the audio file.
