import streamlit as st
import graphviz

# Title of the application
st.title("🍃 Understanding English Syllables")

# Create two tabs: 
tab1, tab2, tab3 = st.tabs(["Syllable Structure", "Tab2", "Tab3"])

# Define the content of each tab
with tab1:
    st.markdown("The user can visualize the syllable structure of a word transcribed with IPA symbols.")
    
    # Create a link styled as a button that opens the URL in a new tab
    app_url = "https://syllable.streamlit.app/"
    st.markdown(f'<a href="{app_url}" target="_blank" style="display: inline-block; text-decoration: none; background-color: #FF9933; color: white; padding: 10px 20px; border-radius: 5px;">Open Syllable Structure App</a>', unsafe_allow_html=True)

    st.caption("This tool provides a visual syllable structure: syllable, onset, nucleus, rhyme, coda.")

with tab2:
    st.header("TBA")
    st.markdown("TBA")
    

with tab3:

    st.header("TBA")
    
    st.markdown("TBA")
    
    # Create a link styled as a button that opens the URL in a new tab
