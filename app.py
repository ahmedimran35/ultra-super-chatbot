import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
import time

# Set page configuration first
st.set_page_config(page_title="Chat Bot", page_icon=":panda_face:")

# Hide Streamlit elements with custom CSS immediately after page config
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Load environment variables from .env file
load_dotenv()

# Configure the Google AI SDK with the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the generative model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Set up Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Ultra Super AI Chatbot")

# Function to get response from the Gemini model
def get_response(query, chat_history):
    # Prepare the chat history in the required format
    history = [{"parts": [{"text": msg['content']}], "role": "user" if msg['type'] == "human" else "model"} for msg in chat_history]
    chat_session = model.start_chat(history=history)
    try:
        response = chat_session.send_message(query)
        return response.text
    except genai.types.StopCandidateException as e:
        return e.candidate.text

# Typing animation CSS and JS
typing_animation = """
<style>
@keyframes typing {
  from { width: 0 }
  to { width: 100% }
}
@keyframes blink-caret {
  from, to { border-color: transparent }
  50% { border-color: black }
}
.typewriter h1 {
  overflow: hidden;
  border-right: .15em solid black;
  white-space: nowrap;
  margin: 0 auto;
  letter-spacing: .15em;
  animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
}
</style>
"""

loading_animation = """
<style>
@keyframes ldio {
  0% { transform: rotate(0deg) }
  100% { transform: rotate(360deg) }
}
.ldio div {
  box-sizing: border-box!important;
}
.ldio > div {
  position: absolute;
  width: 64px;
  height: 64px;
  margin: 8px;
  border: 8px solid #000;
  border-top-color: transparent;
  border-radius: 50%;
  animation: ldio 1s linear infinite;
}
.ldio {
  width: 80px;
  height: 80px;
  display: inline-block;
  overflow: hidden;
  background: none;
}
.loadingio-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}
</style>
"""

st.markdown(typing_animation, unsafe_allow_html=True)
st.markdown(loading_animation, unsafe_allow_html=True)

# Conversation rendering
for message in st.session_state.chat_history:
    if message['type'] == "human":
        with st.chat_message("Human"):
            st.markdown(message['content'])
    else:
        with st.chat_message("AI"):
            st.markdown(message['content'])

# User input
user_query = st.chat_input("Your Message")

if user_query:
    st.session_state.chat_history.append({"type": "human", "content": user_query})

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        placeholder = st.empty()
        
        # Show loading animation
        with placeholder.container():
            st.markdown("""
                <div class="loadingio-spinner">
                    <div class="ldio">
                        <div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        ai_response = get_response(user_query, st.session_state.chat_history)
        
        # Add typing effect
        placeholder.markdown(f'<div class="typewriter"><h1>{ai_response}</h1></div>', unsafe_allow_html=True)
        
        # Simulate typing delay
        time.sleep(3.5)
        
        # Update placeholder with the final response
        placeholder.markdown(ai_response)
        
    st.session_state.chat_history.append({"type": "ai", "content": ai_response})

st.snow()
st.balloons()
