import streamlit as st
import speech_recognition as sr
from Levenshtein import ratio
import tempfile
import numpy as np
import pandas as pd

# Sample dataframe with sentences
data = {
    "Sentences": [
        "A stitch in time saves nine.",
        "To be or not to be, that is the question.",
        "Five cats were living in safe caves.",
        "Hives give shelter to bees in large caves.",
        "His decision to plant a rose was amazing.",
        "She sells sea shells by the sea shore.",
        "The colorful parrot likes rolling berries.",
        "Time flies like an arrow; fruit flies like a banana.",
        "Good things come to those who wait.",
        "All human beings are born free and equal in dignity and rights."
    ]
}
df = pd.DataFrame(data)
user_scores = {}

# Function to transcribe audio
def transcribe_audio(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = r.record(source)
    try:
        text = r.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

# Function to calculate pronunciation correction
def pronunciation_correction(name, expected_text, audio_file):
    user_spoken_text = transcribe_audio(audio_file)
    similarity = ratio(expected_text.lower(), user_spoken_text.lower())
    score = float(f"{similarity:.2f}")
    
    if name in user_scores:
        user_scores[name].append(score)
    else:
        user_scores[name] = [score]
    
    feedback = "Excellent pronunciation!" if score >= 0.9 else \
               "Good pronunciation!" if score >= 0.7 else \
               "Needs improvement." if score >= 0.5 else \
               "Maybe you said something different? Try again focusing more on clarity."
    return feedback, score

# Function to calculate average score
def calculate_average(name):
    if name in user_scores and user_scores[name]:
        filtered_scores = [score for score in user_scores[name] if score > 0]  # Ignore zeros
        average_score = sum(filtered_scores) / len(filtered_scores)
    else:
        average_score = 0
    return f"Great job, {name}! Your average score is: {average_score:.2f}. Keep practicing to improve further!"

# Convert MP3 to WAV function
def convert_to_wav(audio_file):
    try:
        sound = AudioSegment.from_mp3(audio_file)
        buffer = io.BytesIO()
        sound.export(buffer, format="wav")
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"An error occurred: {str(e)}. This format may require external dependencies not available in this environment.")
        
# Streamlit app layout
st.title("Pronunciation Feedback")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎵 Recording", "🎶 MP3-to-WAV", "🌀 Accuracy Feedback", "Temporary"])


# Tab 1: Recording
with tab1:
    st.caption("Make sure to give this app permission to access microphone in your device.")
    
    # Create a link styled as a button that opens the URL in a new tab
    mic_url = "https://mk-316-recorder.hf.space/"
    st.markdown(f'<a href="{mic_url}" target="_blank" style="display: inline-block; text-decoration: none; background-color: #FF9933; color: white; padding: 10px 20px; border-radius: 5px;">Open Recorder App</a>', unsafe_allow_html=True)


# Tab 2: MP3 to WAV Converter
with tab2:
    st.header("MP3 to WAV Converter")
    audio_file = st.file_uploader("Upload MP3 file", type=['mp3'])

    if audio_file is not None:
        wav_buffer = convert_to_wav(audio_file)
        if wav_buffer is not None:
             st.audio(wav_buffer, format='audio/wav')

# Tab 3: Accuracy Feedback
with tab3:
    st.header("Accuracy feedback: Overview")
    st.caption("When you click on the app below, you will be able to select a sentence and record it. After recording, pressing the 'submit' button will display simple feedback and a score. The scores range from 0 to 1, and a score of 0.9 or higher indicates that the sentence is clearly recognizable. (Note: The scores are calculated using the Levenshtein distance.)")
    ext_url = "https://mk-316-pronunciationfeedback.hf.space"
    st.markdown(f'<a href="{ext_url}" target="_blank" style="display: inline-block; text-decoration: none; background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 5px;">Click to Open Application</a>', unsafe_allow_html=True)



with tab4:
    st.subheader("Temp: Check Your Pronunciation Accuracy")
    
    # User inputs
    name = st.text_input("Enter your name", placeholder="Type your name here...")
    sentence = st.selectbox("Select a Sentence", df['Sentences'].tolist())
    st.write("Selected Sentence:", sentence)
    
    # Audio upload
    audio_file = st.file_uploader("Upload your audio file (WAV format)", type=["wav"])

    # Button to check pronunciation
    if st.button("Check Pronunciation"):
        if name and audio_file and sentence:
            with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as tmpfile:
                tmpfile.write(audio_file.read())
                tmpfile.seek(0)
                feedback, score = pronunciation_correction(name, sentence, tmpfile.name)
                st.write("Pronunciation Feedback:", feedback)
                st.write("Pronunciation Accuracy Score:", score)
        else:
            st.warning("Please enter your name, select a sentence, and upload an audio file.")
    
    # Button to show average score
    if st.button("Show Average Score"):
        if name:
            avg_score = calculate_average(name)
            st.write(avg_score)
        else:
            st.warning("Please enter your name to calculate the average score.")
