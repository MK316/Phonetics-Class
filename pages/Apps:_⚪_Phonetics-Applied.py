import streamlit as st
import numpy as np
import librosa
import plotly.graph_objs as go
from io import BytesIO
import soundfile as sf

# Title of the app
st.title("Your Voice Pitch")
st.caption("Fundamental Frequency (F0) Estimation")
st.write("Record the following sentence and upload the audio in wav format:")

st.markdown("### '_Moments of meaning emerge when we listen to the sound of the heart._'")

# Create two tabs: Upload and View Results
tab1, tab2 = st.tabs(["Upload Audio", "View Results"])

# Step 1: Upload or record audio file
with tab1:
    st.header("Upload an audio file")
    uploaded_file = st.file_uploader("Upload an audio file in .wav format", type=["wav"])
    
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        temp_file_path = "temp_audio_file.wav"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())
        
        st.audio(temp_file_path, format="audio/wav")
        
        # Load audio data using librosa
        try:
            audio_data, sr = librosa.load(temp_file_path, sr=None)  # Load without resampling
            
            # Compute the fundamental frequency (F0)
            fmin = 50  # Minimum expected frequency (e.g., typical human pitch range)
            fmax = 300  # Maximum expected frequency

            f0, voiced_flag, voiced_probs = librosa.pyin(audio_data, fmin=fmin, fmax=fmax, sr=sr)

            # Store F0 and other info in session state
            st.session_state['f0'] = f0
            st.session_state['sr'] = sr
            st.session_state['audio_data'] = audio_data
            
        except Exception as e:
            st.error(f"An error occurred while processing the audio: {e}")

# Step 2: View the Results in tab 2
with tab2:
    st.header("Results")

    if 'f0' in st.session_state:
        f0 = st.session_state['f0']
        sr = st.session_state['sr']

        # Prepare the plot using Plotly for interactivity
        times = librosa.times_like(f0, sr=sr)
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=times, y=f0, mode='lines', name='F0 (Fundamental Frequency)', line=dict(color='red')))
        
        fig.update_layout(
            title="Fundamental Frequency (F0)",
            xaxis_title="Time (s)",
            yaxis_title="Frequency (Hz)",
            yaxis_range=[0, 300],  # Limiting y-axis to 0 to 300 Hz
            xaxis_rangeslider_visible=True  # Enable range slider to scroll over time
        )

        # Display the interactive plot using Plotly
        st.plotly_chart(fig)

        # Display approximate average F0
        if np.any(f0):
            avg_f0 = np.nanmean(f0)  # Use nanmean to avoid NaN values when calculating the average
            st.write(f"Approximate average fundamental frequency (F0): {avg_f0:.2f} Hz")
        else:
            st.write("F0 could not be estimated from the audio.")
    else:
        st.write("No results to display. Please upload and process audio in the previous tab.")
