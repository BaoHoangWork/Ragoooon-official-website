import streamlit as st
from openai import OpenAI
import requests
import json
import time

st.title("💬 Ragooon")

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
    chat_container = st.container()  # Create a container for the chat history.
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    input_container = st.empty()

    with input_container:
    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
        if prompt := st.chat_input("What can I help you today?", key=1):
        
            # Store and display the current prompt.
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
    
    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt1 := st.chat_input("What can I help you today?", key=2):
    
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
    
    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt2 := st.chat_input("What can I help you today?", key=3):
    
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
