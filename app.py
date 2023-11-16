import streamlit as st
import os
from helpers.utils import get_current_month
from helpers.tone_styling import tone_styling
from helpers.generate_full_text import generate_full_text
from helpers.generate_thumbnail import generate_image
from helpers.audio import generate_audio, add_background_music

##### Define state variables #####
if 'full_text' not in st.session_state:
    st.session_state.full_text = "" 
if 'generate_clicked' not in st.session_state:
    st.session_state.generate_clicked = False
if 'podcast_audio' not in st.session_state:
    st.session_state.podcast_audio = None
if 'condition' not in st.session_state:
    st.session_state.condition = None
if 'links' not in st.session_state:
    st.session_state.links = []
if 'titles' not in st.session_state:
    st.session_state.titles = []
if 'keywords' not in st.session_state:
    st.session_state.keywords = []
##### Define state variables #####

##### Title and Sidebar #####
st.title("Insights For Me")
st.sidebar.title("Settings")
##### Title and Sidebar #####

##### Sidebar Content #####
# Capture user inputs in a sidebar

user_name = st.sidebar.text_input("Enter your name:", "MLReplier")
month = get_current_month()
conditions = ["LLM", "medicine", "sustainable architecture", "cars"]
condition = st.sidebar.selectbox("Enter the topic or condition you're interested in:", conditions)
tone = st.sidebar.selectbox("Tone:", ["Formal", "George Carlin", "Atul Gawande - Short", "Donald Trump - Short"])

# Update condition in session state
st.session_state.condition = condition

st.sidebar.write("")
st.sidebar.write("")

# Button to generate text insights
generate_text_btn = st.sidebar.button("Generate Insights")
generate_podcast_btn = st.sidebar.button("Generate Podcast")

##### Sidebar Content #####

##### Greetings Title #####
st.markdown(f"""
        <h2>Hello <span style='color: #3a86ff;'>{user_name}</span>! <br> 
        Below you can find your <span style='color: #8338ec;'>{month}</span> 
        dose of research on the topic of <span style='color: #ff006e;'>{condition}</span></h2>
        """, unsafe_allow_html=True)
##### Greetings Title #####


##### Text Insights Generation #####
# Remember that the button has been clicked
if generate_text_btn:
    st.session_state.generate_clicked = True

    # Generate thumbnail
    #thumbnail = generate_image(condition)
    #st.image(thumbnail)

    # Generate text
    full_text, links, titles, keywords = generate_full_text(user_name, month, st.session_state.condition)

    if tone != "Formal":
        full_text = tone_styling(full_text, tone)

    # Update session state
    st.session_state.full_text = full_text
    st.session_state.links = links
    st.session_state.titles = titles
    st.session_state.keywords = keywords

# Display the generated text
if st.session_state.generate_clicked:
    st.write(st.session_state.full_text)

    for i, l in enumerate(st.session_state.links):
        with st.expander(f"{st.session_state.titles[i]}"):
            st.markdown(l, unsafe_allow_html=True)
            if st.session_state.keywords:
                st.markdown("Main keyword: " + st.session_state.keywords[i]['main_keyword'])

    st.write("")
    st.write("")
    st.write("")
    st.write("")    
##### Text Insights Generation #####

##### Podcast Generation #####
if generate_podcast_btn:
    # Call the audio generation function only if full_text is available
    if st.session_state.full_text:
        generate_audio(st.session_state.full_text, "/audio")
        st.session_state.podcast_audio = add_background_music("media/voice.mp3", "media/music.mp3", "media/combined.mp3", delay_seconds=5)
        st.audio("media/combined.mp3", format="audio/mp3", start_time=0)
    else:
        st.warning("Please generate insights before creating a podcast.")
##### Podcast Generation #####