
import os
import numpy as np
import sys


# Determine the absolute path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the src directory to the Python path
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Now try to import the load_config function from util
try:
    from util import load_config
    # Import the ModelWrapper classes
    from audio_stem_separation import SpleeterWrapper, DemucsWrapper, OpenUnmixWrapper

except ImportError as e:
    print(f"Error importing module: {e}")
    sys.exit(1)


# Load the configuration
config = load_config()

# Access the input and output directories
config_input_dir = config.get('input_dir')
config_output_dir = config.get('output_dir')


def test_model_wrapper(wrapper, audio_file, output_dir):
    # Load the audio file
    print(f"Testing {wrapper.__class__.__name__}...")
    audio = wrapper.load_audio(audio_file)
    
    # # Check if audio was loaded successfully
    # if isinstance(audio, np.ndarray):
    #     print(f"Audio loaded successfully: {audio.shape}")
    # else:
    #     print("Failed to load audio.")
    
    # Perform separation
    stems = wrapper.separate_stems(audio)
    
    # Check if stems were separated successfully
    if isinstance(stems, dict) and stems:
        print(f"Stems separated successfully: {list(stems.keys())}")
    else:
        print("Failed to separate stems.")
    
    # Save the separated stems
    wrapper.save_stems(stems, output_dir)
    print(f"Stems saved to {output_dir}")

def main():
    # Path to an example audio file (update this with your own path)
    audio_file = os.path.join(config_input_dir,"PACKS - Missy.mp3")
    
    # Output directories
    output_dirs = {
        "spleeter": os.path.join(config_output_dir,"output_spleeter"),
        "demucs": os.path.join(config_output_dir,"output_demucs"),
        "openunmix": os.path.join(config_output_dir,"output_openunmix")
    }

    # Create instances of each wrapper
    # spleeter_wrapper = SpleeterWrapper()
    # demucs_wrapper = DemucsWrapper()
    openunmix_wrapper = OpenUnmixWrapper()

    # Test each model wrapper
    # test_model_wrapper(spleeter_wrapper, audio_file, output_dirs["spleeter"])
    # test_model_wrapper(demucs_wrapper, audio_file, output_dirs["demucs"])
    test_model_wrapper(openunmix_wrapper, audio_file, output_dirs["openunmix"])

if __name__ == "__main__":
    main()
