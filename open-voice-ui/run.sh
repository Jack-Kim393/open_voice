
#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t open-voice-ui .

# Run the Docker container
echo "Running Docker container..."
docker run -p 5000:5000 open-voice-ui
