
import os
import torch
import uuid
from openvoice import se_extractor
from openvoice.api import BaseSpeakerTTS, ToneColorConverter

# Base directory of the script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Paths using absolute paths
ckpt_base = os.path.join(base_dir, 'OpenVoice/checkpoints/base_speakers/EN')
ckpt_converter = os.path.join(base_dir, 'OpenVoice/checkpoints/converter')
output_dir = os.path.join(base_dir, 'outputs')

# Device
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"OpenVoice running on device: {device}")

# Load models
base_speaker_tts = BaseSpeakerTTS(f'{ckpt_base}/config.json', device=device)
base_speaker_tts.load_ckpt(f'{ckpt_base}/checkpoint.pth')

tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

os.makedirs(output_dir, exist_ok=True)

def clone_voice(text, reference_speaker_path, style_reference_path=None):
    """
    Clones a voice from a reference audio file and generates speech from text.
    Optionally uses a style reference audio for the speech style.
    """
    try:
        # Get the target speaker embedding for the voice tone.
        target_se, audio_name = se_extractor.get_se(reference_speaker_path, tone_color_converter, target_dir=os.path.join(base_dir, 'processed'), vad=False)

        # Get the source speaker embedding for the speech style.
        if style_reference_path:
            source_se, _ = se_extractor.get_se(style_reference_path, tone_color_converter, target_dir=os.path.join(base_dir, 'processed'), vad=False)
        else:
            source_se = torch.load(f'{ckpt_base}/en_default_se.pth').to(device)

        # Generate unique filenames to avoid race conditions
        unique_id = uuid.uuid4()
        tmp_path = os.path.join(output_dir, f'tmp_{unique_id}.wav')
        save_path = f'cloned_{unique_id}.wav'
        full_save_path = os.path.join(output_dir, save_path)
        
        base_speaker_tts.tts(text, tmp_path, speaker='default', language='English', speed=1.0)

        # Convert the temporary audio file to the target's voice and style
        encode_message = "@MyShell"
        tone_color_converter.convert(
            audio_src_path=tmp_path, 
            src_se=source_se, 
            tgt_se=target_se, 
            output_path=full_save_path,
            message=encode_message)
        
        # Clean up the temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            
        return save_path
    except Exception as e:
        print(f"Error during voice cloning: {e}")
        return None
