# recognize.py
import numpy as np
from enroll import extract_embedding, load_database

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recognize_speaker(file_path, threshold=0.70):
    test_embedding = extract_embedding(file_path)
    database = load_database()

    best_match = None
    best_score = -1

    for name, db_embedding in database.items():
        score = cosine_similarity(test_embedding, db_embedding)
        if score > best_score:
            best_score = score
            best_match = name

    print("bestscore: ",best_score)
    print("threshold: ",threshold)

    if best_score >= threshold:
        return best_match, best_score
    else:
        return "Unknown", best_score

