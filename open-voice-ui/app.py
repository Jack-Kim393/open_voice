
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from voice_cloner import clone_voice

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure the upload and output directories exist
base_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(base_dir, UPLOAD_FOLDER), exist_ok=True)
os.makedirs(os.path.join(base_dir, OUTPUT_FOLDER), exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'voice_file' not in request.files:
        return jsonify({'error': 'No voice file provided'}), 400
    
    voice_file = request.files['voice_file']
    style_file = request.files.get('style_file') # Use .get() for optional file
    text = request.form.get('text')

    if voice_file.filename == '':
        return jsonify({'error': 'No selected file for tone color'}), 400

    if voice_file and text:
        # Save the main voice file (for tone color)
        voice_filename = voice_file.filename
        voice_filepath = os.path.join(app.config['UPLOAD_FOLDER'], voice_filename)
        voice_file.save(voice_filepath)

        # Save the style reference file if it exists
        style_filepath = None
        if style_file and style_file.filename != '':
            style_filename = style_file.filename
            style_filepath = os.path.join(app.config['UPLOAD_FOLDER'], style_filename)
            style_file.save(style_filepath)

        # Call the voice cloning function with both paths
        output_path = clone_voice(text, voice_filepath, style_reference_path=style_filepath)

        if output_path:
            return jsonify({'audio_file': f'outputs/{output_path}'})
        else:
            return jsonify({'error': 'Failed to clone voice'}), 500

    return jsonify({'error': 'Invalid request'}), 400

@app.route('/outputs/<path:filename>')
def serve_output_file(filename):
    # This needs to know the absolute path of the output directory
    output_dir_absolute = os.path.join(os.path.dirname(os.path.abspath(__file__)), app.config['OUTPUT_FOLDER'])
    return send_from_directory(output_dir_absolute, filename)

def warm_up():
    """Pre-loads all models to prevent cold-start delay on first request."""
    print("Starting model warm-up...")
    try:
        dummy_text = "This is a warm-up call to load the models."
        dummy_reference_audio = os.path.join(base_dir, 'OpenVoice/resources/demo_speaker0.mp3')
        
        if not os.path.exists(dummy_reference_audio):
            print(f"Warm-up audio not found at {dummy_reference_audio}, skipping warm-up.")
            return

        generated_file = clone_voice(dummy_text, dummy_reference_audio)
        
        if generated_file:
            # Clean up the generated warm-up file
            try:
                os.remove(os.path.join(base_dir, OUTPUT_FOLDER, generated_file))
                print("Model warm-up successful.")
            except OSError as e:
                print(f"Error cleaning up warm-up file: {e}")
        else:
            print("Model warm-up failed.")
    except Exception as e:
        print(f"An error occurred during model warm-up: {e}")

if __name__ == '__main__':
    # Warm up the models before starting the server
    with app.app_context():
        warm_up()
    app.run(debug=True, port=5000)
