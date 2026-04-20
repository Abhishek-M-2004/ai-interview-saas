import streamlit as st
from groq import Groq
import os
import psutil

# Page Config
st.set_page_config(page_title="AI Interview Pro", page_icon="🎓")

# SaaS Secret Management (Streamlit Version)
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Initialize Session State for Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for Telemetry & Role Selection
with st.sidebar:
    st.title("Cloud Dashboard")
    role = st.selectbox("Target Job Role", ["Software Engineer", "Data Scientist", "Cloud Architect"])
    
    # Telemetry (Stable Refresh)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    st.metric("Container CPU", f"{cpu}%")
    st.metric("Container RAM", f"{ram}%")
    
    if st.button("Reset Interview"):
        st.session_state.messages = []
        st.rerun()

st.title("🎓 AI Interview Practice SaaS")
st.caption("Real-time Interview Coaching powered by Groq LPU™ Infrastructure")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Your response (Type 'Start' to begin)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response Logic
    with st.chat_message("assistant"):
        try:
            # Building the prompt context
            context = [{"role": "system", "content": f"You are a technical interviewer for a {role} role. Ask one question at a time."}]
            context.extend(st.session_state.messages)
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=context
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Cloud API Error: {e}")
