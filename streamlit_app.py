import streamlit as st
import requests
import json
import time
from streamlit_float import *
from deep_translator import GoogleTranslator

language_mapping = {
    "English": "en",
    "Spanish": "es",
    "Vietnamese": "vi",
    "Russian": "ru",
    "Arabic": "ar",
    "Chinese": "zh-CN",
    "German": "de",
    "Japanese": "ja",
    "Hindi": "hi",
    "Korean": "ko"
}

if "language" not in st.session_state:
    st.session_state.language = "English"

def _(content, target_lang=language_mapping[st.session_state.language]):
    return GoogleTranslator(source='auto', target=target_lang).translate(content)

# Sidebar for language selection
st.sidebar.title(_("Language Selector"))
selected_language = st.sidebar.selectbox(
    "Choose a language to translate", 
    ["English", "Spanish", "Vietnamese", "Russian", "Arabic", "Chinese", "German", "Japanese", "Hindi", "Korean"],  # Language names
    index=["English", "Spanish", "Vietnamese", "Russian", "Arabic", "Chinese", "German", "Japanese", "Hindi", "Korean"].index(st.session_state.language),  # Match the name
    key="language"
)

# Update language in session state
if st.session_state.language != selected_language:
    st.session_state.language = selected_language
    st.experimental_rerun()

st.title(_("❄️ Ragooon ❄️"))
st.subheader(_("Your personal pocket guide dog 🦮"))
float_init(theme=True, include_unstable_primary=False)

st.write(_(
    "A guide dog just for you, talk to Ragooon now! 💬 "
))
    
# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages2" not in st.session_state:
    st.session_state.messages2 = []

# Display the existing chat messages via `st.chat_message`.
for message2 in st.session_state.messages2:
    with st.chat_message(message2["role"]):
        st.markdown(message2["content"])

with st.container():
    prompt2 = st.chat_input(placeholder='What can I help you today?', key=3) 
    button_b_pos = "1rem"
    button_css = float_css_helper(width="2.2rem", bottom=button_b_pos, transition=0)
    float_parent(css=button_css)
    
if prompt2:
    # Store and display the current prompt.
    st.session_state.messages2.append({"role": "user", "content": prompt2})
    with st.chat_message("user"):
        st.markdown(prompt2)

    url = 'https://ragoooon.onrender.com/stream_rag'
    myobj = {"prompts": prompt2, "history": st.session_state.messages2}
    with st.spinner('Ragooon is sniffing'):
        stream = requests.post(url, json = myobj)
    
    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    
    def stream_data():
        for word in stream.json()['stream']:
            yield word
            time.sleep(0.02)
    
    with st.chat_message("assistant"):
        response = st.write_stream(stream_data)
    st.session_state.messages2.append({"role": "assistant", "content": response})
