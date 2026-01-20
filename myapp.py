import streamlit as st
st.title("What can I help with?")
import os
import html
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
    page_title="Chat AI",
    page_icon="💬",
    layout="centered"
)

# -------------------- CUSTOM CSS (Modern Glass UI) --------------------
st.markdown("""
<style>
/* Background */
[data-testid="stAppViewContainer"]{
  background: radial-gradient(1200px 600px at 20% 10%, rgba(0,198,255,.25), transparent 60%),
              radial-gradient(1000px 700px at 80% 20%, rgba(255,0,255,.18), transparent 55%),
              linear-gradient(135deg, #0b1220, #0f2430 35%, #0a0f1a);
}

/* Transparent Streamlit header */
[data-testid="stHeader"]{ background: rgba(0,0,0,0); }
[data-testid="stToolbar"]{ right: 1rem; }

/* Centered layout width */
.block-container{
  max-width: 920px;
  padding-top: 2.0rem;
  padding-bottom: 6rem; /* room for chat input */
}

/* Glass card */
.glass-card{
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 18px;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 18px 60px rgba(0,0,0,.35);
  padding: 18px 18px;
}

/* Title */
.chat-ai-title{
  font-size: 2.1rem;
  font-weight: 800;
  letter-spacing: .2px;
  margin-bottom: .15rem;
  background: linear-gradient(90deg,#00c6ff,#a855f7,#ff4fd8);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}
.chat-ai-subtitle{ color: rgba(255,255,255,.78); margin-top: 0; }

/* Chat message spacing */
[data-testid="stChatMessage"]{
  border-radius: 14px;
  padding: 6px 2px;
}

/* User message bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"]{
  background: linear-gradient(135deg, rgba(0,198,255,.95), rgba(0,114,255,.95));
  padding: 12px 14px;
  border-radius: 16px;
  color: white;
  border: 1px solid rgba(255,255,255,.18);
}

/* Assistant message bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"]{
  background: rgba(255,255,255,.10);
  padding: 12px 14px;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,.12);
  color: rgba(255,255,255,.92);
}

/* Sidebar glass */
section[data-testid="stSidebar"] > div{
  background: rgba(10,15,26,.65);
  border-right: 1px solid rgba(255,255,255,.08);
  backdrop-filter: blur(14px);
}

/* Buttons */
.stButton button{
  border-radius: 12px !important;
  border: 1px solid rgba(255,255,255,.16) !important;
  background: rgba(255,255,255,.08) !important;
}
.stButton button:hover{
  background: rgba(255,255,255,.14) !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
<div class="glass-card">
  <div class="chat-ai-title">Chat AI</div>
  <div class="chat-ai-subtitle">Fast • Smart • Minimal</div>
</div>
""", unsafe_allow_html=True)

st.write("")  # spacer

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("⚙️ Chat AI Settings")
    temperature = st.slider("Creativity", 0.0, 1.5, 0.9)
    max_tokens = st.slider("Max Tokens", 256, 2048, 1024)

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -------------------- CHAT MEMORY --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are Chat AI, a helpful assistant. Be concise, clear, and friendly."
}

# -------------------- DISPLAY CHAT (Streamlit native chat UI) --------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------- INPUT --------------------
prompt = st.chat_input("Message Chat AI...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prevent unbounded growth (keeps UI fast and avoids context overflow)
    MAX_MESSAGES = 30
    st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

    messages_for_api = [SYSTEM_PROMPT] + st.session_state.messages

    try:
        with st.spinner("Chat AI is thinking..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages_for_api,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    except Exception as e:
        st.error(e)

