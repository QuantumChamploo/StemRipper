import torchaudio
from openunmix import predict
from openunmix import umx
import openunmix
import os
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
    
except ImportError as e:
    print(f"Error importing module: {e}")
    sys.exit(1)


# Load the configuration
config = load_config()

# Access the input and output directories
config_input_dir = config.get('input_dir')
config_output_dir = config.get('output_dir')

def separate_audio(input_file, output_dir, model_name='umxhq'):
    """
    Separates an audio file into individual components using OpenUnmix.
    
    Args:
    - input_file (str): Path to the input MP3 file.
    - output_dir (str): Directory where the separated tracks will be saved.
    - model_name (str): The name of the pre-trained model to use (default is 'umxhq').
    """
    # Load the model
    model = openunmix.load_model(model_name)
    
    # Load the audio file
    waveform, sr = torchaudio.load(input_file)
    
    # Ensure the audio is stereo
    if waveform.shape[0] == 1:
        waveform = waveform.repeat(2, 1)
    
    # Perform the separation
    separated_sources = predict.separate(audio=waveform, rate=sr, model=model)
    
    # Save the separated sources
    os.makedirs(output_dir, exist_ok=True)
    for target, audio in separated_sources.items():
        output_path = os.path.join(output_dir, f"{target}.wav")
        torchaudio.save(output_path, audio, sr)
        print(f"Saved {target} to {output_path}")

if __name__ == "__main__":
    # Example usage
    input_file = os.path.join(config_input_dir,"PACKS - Missy.mp3")  # Replace with your input file path
    output_dir = os.path.join(config_output_dir,"output_openunmix") # Replace with your desired output directory

    separate_audio(input_file, output_dir)
