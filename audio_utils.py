import os
import torchaudio
import sounddevice as sd
from scipy.io.wavfile import write

SAMPLE_RATE = 16000
DURATION = 5

def record_audio(filename="output.wav"):
    print("Recording...")
    audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    write(filename, SAMPLE_RATE, audio)
    print(f"Saved to {filename}")
    return filename

def load_audio(path):
    signal, sr = torchaudio.load(path)
    return signal, sr
