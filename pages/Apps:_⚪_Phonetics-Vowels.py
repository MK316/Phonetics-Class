import streamlit as st

# Title of the application
st.title("🍃 Phonetics Learning Tools")

# Create two tabs: 'Vowel Chart' and 'V-description app'
tab1, tab2, tab3 = st.tabs(["Vowel Chart", "V-description app", "Audio & stressed vowels"])

# Define the content of each tab
with tab1:
    st.header("Vowel Chart with Formants (F1 and F2)")
    st.markdown("This tool provides a vowel chart for phonetics practice.")
    
    # Create a link styled as a button that opens the URL in a new tab
    vowel_chart_url = "https://vowelchart.streamlit.app"
    st.markdown(f'<a href="{vowel_chart_url}" target="_blank" style="display: inline-block; text-decoration: none; background-color: #FF9933; color: white; padding: 10px 20px; border-radius: 5px;">Open Vowel Charting App</a>', unsafe_allow_html=True)

    st.caption("This tool provides a vowel chart based on formants (F1, F2).")

with tab2:
    st.header("Vowel description application 1")
    st.markdown("Practice how to describe English vowels.")
    
    # Create a link styled as a button that opens the URL in a new tab
    vowel_chart_url = "https://vowelpractice.streamlit.app/"
    st.markdown(f'<a href="{vowel_chart_url}" target="_blank" style="display: inline-block; text-decoration: none; background-color: #006666; color: white; padding: 10px 20px; border-radius: 5px;">Open Vowel Charting App</a>', unsafe_allow_html=True)

    st.caption("For General American Engilsh Vowels (e.g., 10 Monophthongs and 5 Diphthongs)")
    st.caption("This app will display a vowel IPA symbol. The user will choose the phonetic description of the given vowel in terms of vowel height, backness, roundedness, and tense/lax categories. Scores will be updated.")

with tab3:

    st.header("Listen and Identify the Stressed Vowel")
    
    st.markdown("Listen to the audio and identify the stressed vowel in given words.")
    
    # Create a link styled as a button that opens the URL in a new tab
    vowel_chart_url = "https://identify-vowels.streamlit.app/"
    st.markdown(f'<a href="{vowel_chart_url}" target="_blank" style="display: inline-block; text-decoration: none; background-color: #99CCFF; color: white; padding: 10px 20px; border-radius: 5px;">Open Vowel Identification App</a>', unsafe_allow_html=True)

    st.caption("For General American Engilsh Vowels (e.g., 10 Monophthongs and 5 Diphthongs)")
    st.caption("You'll listen to an audio and practice identifying the stressed vowel in a given English word.")
