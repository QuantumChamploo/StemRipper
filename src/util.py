import json
import os

def load_config():
    """
    Loads the configuration from the config.json file located in the project root directory.

    Returns:
        dict: Configuration data loaded from config.json.

    Raises:
        FileNotFoundError: If the config.json file does not exist.
        ValueError: If the config.json file is empty or contains invalid JSON.
    """
    # Determine the path to the config.json file
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(project_root, 'config.json')

    # Check if the config file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")

    # Load and return the config data
    with open(config_path, 'r') as config_file:
        try:
            config = json.load(config_file)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in the config file: {config_path}")

    return config
