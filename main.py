import streamlit as st
import os
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
from enroll import enroll_speaker
from identify import recognize_speaker


# ===== CONFIG =====
BASE_DIR = "enrollments"
os.makedirs(BASE_DIR, exist_ok=True)
SAMPLE_RATE = 16000
RECORD_SECONDS = 7

def record_audio_fixed_duration(filename, duration=7, sample_rate=16000):
    """Record audio for a fixed duration and save to a file."""
    st.info(f"🎙 Recording for {duration} seconds... Please speak clearly.")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, sample_rate, recording)
    st.success(f"✅ Recording saved: {filename}")

# ===== STREAMLIT APP =====
st.title("🎙️ Voice-based Speaker System")

# Always show mode selector
choice = st.radio("Choose Action", ["Enroll New Speaker", "Identify Speaker"])

# Track recordings in session state
if "recordings_done" not in st.session_state:
    st.session_state.recordings_done = 0

# ---------------- ENROLLMENT ----------------
if choice == "Enroll New Speaker":
    name = st.text_input("Enter speaker name")
    if name:
        user_folder = os.path.join(BASE_DIR, name)
        os.makedirs(user_folder, exist_ok=True)

        st.write("📢 You will need to record **4 samples**, each 5–7 seconds long.")

        if st.session_state.recordings_done < 4:
            if st.button(f"Record Sample {st.session_state.recordings_done + 1}"):
                file_path = os.path.join(user_folder, f"sample_{st.session_state.recordings_done + 1}.wav")
                record_audio_fixed_duration(file_path, duration=RECORD_SECONDS, sample_rate=SAMPLE_RATE)
                st.session_state.recordings_done += 1

        if st.session_state.recordings_done == 4:
            st.success("✅ All 4 recordings completed!")
            if st.button("Enroll Now"):
                for i in range(1, 5):
                    path = os.path.join(user_folder, f"sample_{i}.wav")
                    enroll_speaker(name, path)
                st.success(f"🎯 Successfully enrolled {name}!")
                st.session_state.recordings_done = 0  # reset so we can enroll another user or switch modes

# ---------------- IDENTIFICATION ----------------
elif choice == "Identify Speaker":
    st.write("📢 Speak for **5–7 seconds** for identification.")
    if st.button("Record & Identify"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            temp_path = tmpfile.name
        record_audio_fixed_duration(temp_path, duration=RECORD_SECONDS, sample_rate=SAMPLE_RATE)

        result, score = recognize_speaker(temp_path)
        st.success(f"🎯 Identified: {result} (Score: {score:.2f})")



