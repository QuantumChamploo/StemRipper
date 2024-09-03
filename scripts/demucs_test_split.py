import os
import subprocess
import sys

import torchaudio
torchaudio.set_audio_backend("soundfile")


# Determine the absolute path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the src directory to the Python path
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Now try to import the load_config function from util
try:
    from util import load_config
    
except ImportError as e:
    print(f"Error importing module: {e}")
    sys.exit(1)


# Load the configuration
config = load_config()

# Access the input and output directories
config_input_dir = config.get('input_dir')
config_output_dir = config.get('output_dir')

def split_audio_with_demucs(input_file, output_dir):
    """
    Splits the given audio file into stems using Demucs and saves them to the output directory.
    
    :param input_file: Path to the input MP3 file.
    :param output_dir: Directory where the output stems will be saved.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Build the command to run Demucs
    command = [
        'demucs',  # Demucs executable command
        '--out', output_dir,  # Output directory
        input_file  # Input MP3 file
    ]
    
    # Run the command
    subprocess.run(command, check=True)
    
    print(f"Stems have been saved to: {output_dir}")

if __name__ == "__main__":
    # Example usage
    input_file = os.path.join(config_input_dir,"Missy.mp3")  # Replace with your input file path
    output_dir = os.path.join(config_output_dir,"output_demucs") # Replace with your desired output directory
    
    split_audio_with_demucs(input_file, output_dir)
