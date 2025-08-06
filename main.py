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








# import streamlit as st
# from enroll import enroll_speaker
# import sounddevice as sd
# import scipy.io.wavfile as wav
# import os
# import time

# # ====== CONFIG ======
# BASE_DIR = "enrollments"  # Where all enrollment folders are stored
# os.makedirs(BASE_DIR, exist_ok=True)
# SAMPLE_RATE = 16000  # 16kHz for voice models
# RECORD_SECONDS = 7   # Each recording duration

# def record_audio_fixed_duration(filename, duration=7, sample_rate=16000):
#     """Record audio for a fixed duration and save to a file."""
#     st.info(f"🎙 Recording for {duration} seconds... Please speak clearly.")
#     recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
#     sd.wait()  # Wait until recording is finished
#     wav.write(filename, sample_rate, recording)
#     st.success(f"✅ Recording saved: {filename}")

# st.title("🎙️ Voice-based Speaker Enrollment")

# name = st.text_input("Enter speaker name")

# if name:
#     user_folder = os.path.join(BASE_DIR, name)
#     os.makedirs(user_folder, exist_ok=True)  # Create a folder for each user

#     st.write("You will need to record **4 samples**, each 7 seconds long.")

#     # Track recorded files in session state
#     if "recordings_done" not in st.session_state:
#         st.session_state.recordings_done = 0

#     # Record button
#     if st.session_state.recordings_done < 4:
#         if st.button(f"Record Sample {st.session_state.recordings_done + 1}"):
#             file_path = os.path.join(user_folder, f"sample_{st.session_state.recordings_done + 1}.wav")
#             record_audio_fixed_duration(file_path, duration=RECORD_SECONDS, sample_rate=SAMPLE_RATE)
#             st.session_state.recordings_done += 1

#     # Enroll after 4 recordings
#     if st.session_state.recordings_done == 4:
#         if st.button("Enroll Now"):
#             for i in range(1, 5):
#                 path = os.path.join(user_folder, f"sample_{i}.wav")
#                 enroll_speaker(name, path)
#             st.success(f"🎯 Successfully enrolled {name} with 4 samples!")











# import streamlit as st
# from audio_recorder_streamlit import audio_recorder
# from enroll import enroll_speaker
# from identify import recognize_speaker
# import tempfile
# import os

# st.title("🎙️ Voice-based Speaker Identification")

# choice = st.radio("Choose Action", ["Enroll New Speaker", "Identify Speaker"])

# if choice == "Enroll New Speaker":
#     name = st.text_input("Enter speaker name")
#     st.write("Click below and speak for 5–7 seconds to enroll.")

#     audio_bytes = audio_recorder(
#         pause_threshold=2.0,  # seconds of silence before stopping
#         sample_rate=16000
#     )

#     if audio_bytes and name:
#         # Save the recorded audio temporarily
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
#             tmpfile.write(audio_bytes)
#             temp_path = tmpfile.name

#         if st.button("Enroll Now"):
#             enroll_speaker(name, temp_path)
#             st.success(f"✅ Enrolled {name}")
#             os.remove(temp_path)

# elif choice == "Identify Speaker":
#     st.write("Click below and speak for identification.")

#     audio_bytes = audio_recorder(
#         pause_threshold=2.0,
#         sample_rate=16000
#     )

#     if audio_bytes:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
#             tmpfile.write(audio_bytes)
#             temp_path = tmpfile.name

#         if st.button("Identify Now"):
#             result = recognize_speaker(temp_path)
#             st.success(f"🎯 Identified: {result}")
#             os.remove(temp_path)


# import streamlit as st
# from audio_utils import record_audio
# from enroll import enroll_speaker
# from identify import recognize_speaker

# st.title("🎙️ Voice-based Speaker Identification")

# choice = st.radio("Choose Action", ["Enroll New Speaker", "Identify Speaker"])

# if choice == "Enroll New Speaker":
#     name = st.text_input("Enter speaker name")
#     if st.button("Record & Enroll"):
#         path = record_audio("temp.wav")
#         enroll_speaker(name, path)
#         st.success(f"Enrolled {name}")

# elif choice == "Identify Speaker":
#     if st.button("Record & Identify"):
#         path = record_audio("temp.wav")
#         result = recognize_speaker(path)
#         st.success(f"Identified: {result}")


# import streamlit as st
# from audio_utils import record_audio
# from enroll import enroll_speaker
# from identify import recognize_speaker

# st.title("🎙️ Voice-based Speaker Identification")

# choice = st.radio("Choose Action", ["Enroll New Speaker", "Identify Speaker"])

# #TODO: speaker enrollment using streamlit
# #TODO: keep the db and recorded audio files in seperate folder

# if choice == "Identify Speaker":
#     if st.button("Record & Identify"):
#         path = record_audio("temp.wav")
#         result = recognize_speaker(path)
#         st.success(f"Identified: {result}")

