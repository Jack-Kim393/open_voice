#!/bin/bash
# This script starts the Open Voice UI application.

# Get the absolute path of the directory where the script is located
BASEDIR=$(cd "$(dirname "$0")" && pwd)

# Change to the script's directory
cd "$BASEDIR"

# Run the Flask application using the Python interpreter from the virtual environment
echo "Starting Open Voice UI..."
echo "Virtual environment Python: ./open-voice-ui/venv/bin/python3"
echo "Application script: ./open-voice-ui/app.py"

./open-voice-ui/venv/bin/python3 ./open-voice-ui/app.py
