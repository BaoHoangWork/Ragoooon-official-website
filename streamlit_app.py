import streamlit as st
import requests
import json
import time
from streamlit_float import *
import gettext
import os

# Setup translation
def set_language(language: str):
    """Set the language for gettext."""
    locales_dir = os.path.join(os.path.dirname(__file__), "locales")
    try:
        lang_translations = gettext.translation("messages", locales_dir, languages=[language])
        lang_translations.install()
        return lang_translations.gettext
    except FileNotFoundError:
        # Fallback to default (English)
        gettext.install("messages", locales_dir)
        return gettext.gettext

# Sidebar for language selection
st.sidebar.title("Language Selector")
if "language" not in st.session_state:
        st.session_state.language = "en"
selected_language = st.sidebar.selectbox(
    "Choose language", 
    ["en", "es", "vn"], 
    index=["en", "es", "vn"].index(st.session_state.language),
    key="language"
)

# Update language in session state
if st.session_state.language != selected_language:
    st.session_state.language = selected_language
    st.experimental_rerun()

# Load translations dynamically for the selected language
_ = set_language(st.session_state.language)

# App content
st.title(_("Welcome to My Streamlit App"))
st.write(_("This app demonstrates how to use gettext for translations."))

st.title("💬 Ragooon")
float_init(theme=True, include_unstable_primary=False)

# tab setups
tab1, tab2, tab3 = st.tabs(["Snowflake Mistral AI /stream_complete", "Testing AI", "/stream_chat"])

# SNOWFLAKE MISTRAL TAB
with tab1:
    # Show title and description.
    st.title("💬 Ragooon Chatbot")
    st.write(
    "API for RagoonBot, a custom snowflake mistral model version 0.1"
    )
    
    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display existing chat messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    with st.container():
        prompt = st.chat_input(placeholder='What can I help you today?', key=1) 
        button_b_pos = "1rem"
        button_css = float_css_helper(width="2.2rem", bottom=button_b_pos, transition=0)
        float_parent(css=button_css)
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        url = 'https://ragoooon.onrender.com/stream_complete'
        myobj = {"prompt": prompt,"history": []}
        stream = requests.post(url, json = myobj)
        
        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        def stream_data():
            for word in stream.json()['stream']:
                yield word
                time.sleep(0.02)
        
        with st.chat_message("assistant"):
            response = st.write_stream(stream_data)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
# TESTING AI TAB
with tab2:
    # Show title and description.
    st.title("💬 Ragooon Chatbot TESTING")
    st.write(
        "API for RagoonBot, a testing model"
    )
        
    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages1" not in st.session_state:
        st.session_state.messages1 = []
    
    # Display the existing chat messages via `st.chat_message`.
    for message1 in st.session_state.messages1:
        with st.chat_message(message1["role"]):
            st.markdown(message1["content"])

    with st.container():
        prompt1 = st.chat_input(placeholder='What can I help you today?', key=2)
        button_b_pos = "1rem"
        button_css = float_css_helper(width="2.2rem", bottom=button_b_pos, transition=0)
        float_parent(css=button_css)
        
    if prompt1:    
        # Store and display the current prompt.
        st.session_state.messages1.append({"role": "user", "content": prompt1})
        with st.chat_message("user"):
            st.markdown(prompt1)
    
        url = 'https://ragoooon.onrender.com/stream_complete'
        myobj = {"prompt": prompt1,"history": []}
        stream = requests.post(url, json = myobj)
        
        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        
        def stream_data():
            for word in stream.json()['stream']:
                yield word
                time.sleep(0.02)
        
        with st.chat_message("assistant"):
            response = st.write_stream(stream_data)
        st.session_state.messages1.append({"role": "assistant", "content": response})

# /stream_chat
with tab3:
    # Show title and description.
    st.title("💬 /stream_chat API")
    st.write(
        "API for RagoonBot, a testing model"
    )
        
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
    
        url = 'https://ragoooon.onrender.com/stream_chat'
        myobj = {"prompt": prompt2, "history": st.session_state.messages2}
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
