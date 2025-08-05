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


import streamlit as st
from audio_utils import record_audio
from enroll import enroll_speaker
from identify import recognize_speaker

st.title("🎙️ Voice-based Speaker Identification")

choice = st.radio("Choose Action", ["Enroll New Speaker", "Identify Speaker"])

#TODO: speaker enrollment using streamlit
#TODO: keep the db and recorded audio files in seperate folder

if choice == "Identify Speaker":
    if st.button("Record & Identify"):
        path = record_audio("temp.wav")
        result = recognize_speaker(path)
        st.success(f"Identified: {result}")

