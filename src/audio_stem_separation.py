
from abc import ABC, abstractmethod
import numpy as np
import os
import soundfile as sf
import torch
import torchaudio
from spleeter.separator import Separator
from demucs import pretrained
from demucs.apply import apply_model
from demucs.audio import AudioFile
from openunmix import predict

class ModelWrapper(ABC):
    @abstractmethod
    def load_audio(self, file_path: str):
        """
        Loads an audio file from the given path and returns it as a numpy array.
        
        Args:
            file_path (str): The path to the audio file.

        Returns:
            np.ndarray: The loaded audio as a numpy array.
        """
        pass

    @abstractmethod
    def separate_stems(self, audio: np.ndarray) -> dict:
        """
        Separates the audio into its component stems.
        
        Args:
            audio (np.ndarray): The audio data to separate.

        Returns:
            dict: A dictionary where keys are stem names and values are numpy arrays of the separated audio.
        """
        pass

    @abstractmethod
    def save_stems(self, stems: dict, output_dir: str) -> None:
        """
        Saves the separated stems to the specified directory.
        
        Args:
            stems (dict): A dictionary of separated stems.
            output_dir (str): The directory where the stems should be saved.
        """
        pass

class SpleeterWrapper(ModelWrapper):
    def __init__(self, stems: int = 4):
        self.separator = Separator(f'spleeter:{stems}stems')

    def load_audio(self, file_path: str) -> np.ndarray:
        audio, _ = sf.read(file_path)
        return audio

    def separate_stems(self, audio: np.ndarray) -> dict:
        stems = self.separator.separate(audio)
        return stems

    def save_stems(self, stems: dict, output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)
        for stem_name, stem_data in stems.items():
            output_path = os.path.join(output_dir, f"{stem_name}.wav")
            sf.write(output_path, stem_data, samplerate=44100)

class DemucsWrapper(ModelWrapper):
    def __init__(self):
        self.model = pretrained.get_model('demucs')
        self.model.to('cuda' if torch.cuda.is_available() else 'cpu')

    def load_audio(self, file_path: str) -> np.ndarray:
        with AudioFile(file_path) as f:
            audio = f.read(self.model.samplerate, self.model.audio_channels)
        return audio

    def separate_stems(self, audio: np.ndarray) -> dict:
        sources = apply_model(self.model, audio)
        stem_names = self.model.sources
        stems = {name: source for name, source in zip(stem_names, sources)}
        return stems

    def save_stems(self, stems: dict, output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)
        for stem_name, stem_data in stems.items():
            output_path = os.path.join(output_dir, f"{stem_name}.wav")
            AudioFile.save(output_path, stem_data, self.model.samplerate)

class OpenUnmixWrapper(ModelWrapper):
    def __init__(self):
        # Initialization specific to Open-Unmix can go here
        pass

    def load_audio(self, file_path: str):
        waveform, sample_rate = torchaudio.load(file_path)
        self.sr = sample_rate
        return waveform

    def separate_stems(self, audio: np.ndarray) -> dict:
        stems = predict.separate(audio,self.sr)
        return stems

    def save_stems(self, stems: dict, output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)
        for stem_name, stem_data in stems.items():
            output_path = os.path.join(output_dir, f"{stem_name}.wav")
            torchaudio.save(output_path, torch.tensor(stem_data), 44100)
