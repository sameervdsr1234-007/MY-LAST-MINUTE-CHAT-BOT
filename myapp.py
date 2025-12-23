import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# -------------------- ENV --------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY missing")
    st.stop()

client = Groq(api_key=api_key)

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Nova AI",
    page_icon="✨",
    layout="centered"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main {
    background-color: transparent;
}

.chat-bubble-user {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    padding: 12px 16px;
    border-radius: 18px;
    color: white;
    margin-bottom: 10px;
    max-width: 75%;
    margin-left: auto;
}

.chat-bubble-ai {
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(10px);
    padding: 12px 16px;
    border-radius: 18px;
    color: #ffffff;
    margin-bottom: 10px;
    max-width: 75%;
}

.header {
    text-align: center;
    font-size: 2.2rem;
    font-weight: bold;
    background: linear-gradient(to right, #00c6ff, #f0f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<div class="header">✨ Nova AI Assistant</div>', unsafe_allow_html=True)
st.caption("Your personal AI • Fast • Smart • Minimal")

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("⚙️ Settings")
    temperature = st.slider("Creativity", 0.1, 1.5, 0.9)
    max_tokens = st.slider("Max Tokens", 256, 2048, 1024)
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -------------------- CHAT MEMORY --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- DISPLAY CHAT --------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="chat-bubble-user">{msg["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-bubble-ai">{msg["content"]}</div>',
            unsafe_allow_html=True
        )

# -------------------- INPUT --------------------
prompt = st.chat_input("Ask something amazing...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        reply = response.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        st.rerun()

    except Exception as e:
        st.error(e)