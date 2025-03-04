import streamlit as st
from groq import Groq
import os

os.environ["GROQ_API_KEY"] = "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"

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Streamlit page config
st.set_page_config(page_title="🏋️ AI Health Coach", page_icon="💬", layout="centered")

# CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #F5F5F5;
        padding: 20px;
    }
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #000000 !important;
    }
    input, textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    button[kind="secondaryFormSubmit"] {
        background-color: #4CAF50 !important;
        color: #FFFFFF !important;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
    }
    button[kind="secondaryFormSubmit"]:hover {
        background-color: #45A049 !important;
    }
    .user-msg {
        background-color: #D0E6FF;
        color: #000000;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
        width: fit-content;
        max-width: 80%;
        font-size: 16px;
    }
    .coach-msg {
        background-color: #FFFFFF;
        color: #000000;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
        width: fit-content;
        max-width: 80%;
        font-size: 16px;
        border: 1px solid #E0E0E0;
    }
    </style>
""", unsafe_allow_html=True)


st.title("🏋️ Your AI Health & Fitness Coach")
st.write("Ask me anything about workouts, nutrition, or staying healthy!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a world-class health and fitness coach. Always give actionable tips for workouts, nutrition, and recovery."}
    ]
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []


#  Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here:", key="user_input")
    send = st.form_submit_button("Send 💬")

if send and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.chat_display.append(f'<div class="user-msg"><strong>You:</strong> {user_input}</div>')

    response = client.chat.completions.create(
        model="llama-3.2-1b-preview",
        messages=st.session_state.messages,
        temperature=0.7
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.chat_display.append(f'<div class="coach-msg"><strong>Coach:</strong> {reply}</div>')


# Display chat history
st.write("---")
for message in reversed(st.session_state.chat_display):
    st.markdown(message, unsafe_allow_html=True)
