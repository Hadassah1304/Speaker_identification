# enroll.py
import os
import pickle
import torchaudio
import torch
import numpy as np
from speechbrain.pretrained import EncoderClassifier

# Load the pretrained model only once
classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_model")
DB_PATH = "speaker_db.pkl"

def load_database():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "rb") as f:
            return pickle.load(f)
    return {}

def save_database(database):
    with open(DB_PATH, "wb") as f:
        pickle.dump(database, f)

def extract_embedding(file_path):
    signal, fs = torchaudio.load(file_path)
    embeddings = classifier.encode_batch(signal)
    return embeddings.squeeze().detach().cpu().numpy()

def enroll_speaker(name, file_path):
    embedding = extract_embedding(file_path)
    database = load_database()
    database[name] = embedding
    save_database(database)

