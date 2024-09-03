import sys
import os


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
input_dir = config.get('input_dir')
output_dir = config.get('output_dir')

print(f"Input Directory: {input_dir}")
print(f"Output Directory: {output_dir}")
