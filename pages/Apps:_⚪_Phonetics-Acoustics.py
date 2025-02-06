import streamlit as st
import numpy as np
from scipy.io.wavfile import write
from io import BytesIO
import librosa
import librosa.display
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def generate_wave(amplitude, frequency, time):
    """Generate sinusoidal wave data based on amplitude, frequency, and time."""
    return amplitude * np.sin(2 * np.pi * frequency * time)

def generate_tone(frequency, duration=1, sample_rate=44100, amplitude=0.3):
    """Generate a pure tone based on the frequency."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = amplitude * np.sin(2 * np.pi * frequency * t)
    tone_int16 = np.int16(tone / np.max(np.abs(tone)) * 32767)  # Convert to 16-bit data
    return tone_int16, t, tone

def plot_spectrogram(audio_path, time_min, time_max, freq_min, freq_max):
    try:
        y, sr = librosa.load(audio_path, sr=None)
        if y.size == 0:
            st.error("Loaded audio is empty. Please check the file and try again.")
            return
        
        start_sample = int(time_min * sr)
        end_sample = int(time_max * sr)

        if start_sample >= end_sample:
            st.error("End time must be greater than start time.")
            return
        if end_sample > len(y):
            st.error("End time exceeds the audio duration.")
            return
        
        y_segment = y[start_sample:end_sample]

        if y_segment.size == 0:
            st.error("Selected audio segment is empty.")
            return

        D = np.abs(librosa.stft(y_segment))
        S_dB = librosa.amplitude_to_db(D, ref=np.max)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='linear', hop_length=512)
        plt.colorbar(format='%+2.0f dB')
        plt.title('Frequency Spectrogram in Hz')
        plt.xlim([0, time_max - time_min])  # Adjust the x-axis to the duration of the segment
        plt.ylim([freq_min, freq_max])
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.tight_layout()
        st.pyplot(plt)

        buffer = BytesIO()
        write(buffer, sr, y_segment.astype(np.int16))
        buffer.seek(0)
        st.audio(buffer, format='audio/wav')

    except Exception as e:
        st.error(f"An error occurred while generating the spectrogram: {str(e)}")


def main():
    st.title('Acoustics')
    tabs = st.tabs(["Introduction", "Generate Tone", "Upload and Analyze Spectrogram","Complex wave"])

    with tabs[0]:
        st.write("Welcome to the Acoustics module. This module allows you to explore various aspects of sound.")

    with tabs[1]:
        st.write("Generate a pure tone based on a specified frequency.")
        freq_input = st.number_input('Enter a frequency (50 to 500 Hz):', min_value=50, max_value=500, value=100, step=1)
        duration_input = st.slider('Duration (seconds):', min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        generate_button = st.button('Generate Tone')

        if generate_button:
            data, t, waveform = generate_tone(freq_input, duration=duration_input)
            buffer = BytesIO()
            write(buffer, 44100, data)
            buffer.seek(0)
            st.audio(buffer, format='audio/wav')

            fig = go.Figure(data=go.Scatter(x=t, y=waveform))
            fig.update_layout(
                title=f"Waveform of the Generated Tone at {freq_input} Hz",
                xaxis_title='Time [s]',
                yaxis_title='Amplitude',
                xaxis_rangeslider_visible=True
            )
            st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        st.header("Upload and Analyze Spectrogram")
        uploaded_file = st.file_uploader("Upload your audio file (WAV format)", type=['wav'])

        if uploaded_file is not None:
            audio_path = 'temp_audio.wav'
            with open(audio_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.success("File uploaded successfully!")
            st.audio(audio_path)  # Play the uploaded audio file immediately

            time_min = st.slider('Start Time (s)', min_value=0.0, max_value=30.0, value=0.0, step=0.1)
            time_max = st.slider('End Time (s)', min_value=0.1, max_value=30.0, value=5.0, step=0.1)
            freq_min = st.slider('Min Frequency (Hz)', min_value=0, max_value=8000, value=0, step=100)
            freq_max = st.slider('Max Frequency (Hz)', min_value=1000, max_value=20000, value=8000, step=100)

            if st.button('Generate Spectrogram'):
                plot_spectrogram(audio_path, time_min, time_max, freq_min, freq_max)

    with tabs[3]:
        st.subheader("Generate a Complex Wave")
        col1, col2 = st.columns(2)
        amp1 = col1.number_input('Amplitude of Wave 1:', value=1.0, format="%.2f")
        freq1 = col2.number_input('Frequency of Wave 1:', value=1.0, format="%.2f")
        
        amp2 = col1.number_input('Amplitude of Wave 2:', value=1.0, format="%.2f")
        freq2 = col2.number_input('Frequency of Wave 2:', value=1.0, format="%.2f")
        
        amp3 = col1.number_input('Amplitude of Wave 3:', value=1.0, format="%.2f")
        freq3 = col2.number_input('Frequency of Wave 3:', value=1.0, format="%.2f")
        
        t_max = st.slider("Select max time for the x-axis:", min_value=1, max_value=10, value=5, step=1)
        
        if st.button('Generate a complex wave'):
            time = np.linspace(0, t_max, 1000)
            wave1 = generate_wave(amp1, freq1, time)
            wave2 = generate_wave(amp2, freq2, time)
            wave3 = generate_wave(amp3, freq3, time)
            complex_wave = wave1 + wave2 + wave3

            # add dash='dash' for each if you want
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=time, y=wave1, mode='lines', name='Wave 1', line=dict(color='#f5c542')))
            fig.add_trace(go.Scatter(x=time, y=wave2, mode='lines', name='Wave 2', line=dict(color='#69f542')))
            fig.add_trace(go.Scatter(x=time, y=wave3, mode='lines', name='Wave 3', line=dict(color='#42d4f5')))  # 'light blue' should be 'lightblue'
            fig.add_trace(go.Scatter(x=time, y=complex_wave, mode='lines', name='Complex Wave', line=dict(color='#4e535c', width=4)))


            fig.update_layout(
                title="Complex Wave Formation",
                xaxis_title="Time",
                yaxis_title="Amplitude",
                xaxis_rangeslider_visible=True
            )
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
