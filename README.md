
# StemRipper

**StemRipper** is a tool for splitting audio files into their individual stems, such as vocals, drums, bass, etc. This project is currently exploring various packages to achieve the best results, with **Demucs** being the only working package at the moment.

## Features
- Split audio files into stems using Demucs.
- Currently supports the following stems:
  - Vocals
  - Drums
  - Bass
  - Other instruments

## Prerequisites

### 1. Python
Ensure you have Python 3.8+ installed on your system.

### 2. FFmpeg
**FFmpeg** is required by `torchaudio` (used by Demucs) to handle audio processing.

#### Installation Instructions:

- **Windows**:
  - Download FFmpeg from the [official website](https://ffmpeg.org/download.html).
  - Extract the files and add the `bin` directory to your system's PATH.
  
- **macOS**:
  - Install via Homebrew:
    ```sh
    brew install ffmpeg
    ```
  
- **Linux**:
  - Install via APT (Debian/Ubuntu):
    ```sh
    sudo apt-get install ffmpeg
    ```

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/StemRipper.git
   cd StemRipper
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```
## Config
We use a config file for local paths to input and output folders. Take the file in 
```config_example.json```
and create a file in the project folder called
```config.json```

## Usage

Current tests script, to split an MP3 file into stems using Demucs, run:

```sh
python scripts/demucs_test_split.py
```

Replace the paths in `scripts/demucs_test_split.py` with your input file and desired output directory.

## Roadmap

- Explore additional packages for stem separation.
- Improve accuracy and performance of stem separation.
- Add support for more file formats and stem types.

## Contributing

Feel free to submit issues and pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for details.
