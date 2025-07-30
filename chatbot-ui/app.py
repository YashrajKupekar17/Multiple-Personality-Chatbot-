import streamlit as st
import requests
import json
from datetime import datetime
from typing import List, Dict
import numpy as np
import logging

# === Logger Setup ===
logging.basicConfig(
    filename="chatbot_app.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(module)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# === Page Configuration ===
st.set_page_config(
    page_title="MPD Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === API Configuration ===
# API_BASE_URL = "http://localhost:8000"  # For local development
API_BASE_URL = "http://api:8000"         # Docker service

# === Session State Initialization ===
if "current_thread" not in st.session_state:
    st.session_state.current_thread = None
if "threads" not in st.session_state:
    st.session_state.threads = set()
if "messages" not in st.session_state:
    st.session_state.messages = {}

# === Helper Functions ===
def send_message_to_api(message: str, thread_id: str) -> str:
    """Send message to the FastAPI backend (Logs thread and character choice)."""
    try:
        charater_id_no = np.random.randint(0, 4)
        available_character_ids = ["motivator", "comedian", "philosopher", "intelligent"]
        selected_character_id = available_character_ids[charater_id_no]
        logging.info(f"Sending message to API | thread_id='{thread_id}', character_id='{selected_character_id}', message='{message[:50]}'")
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={
                "message": message,
                "thread_id": thread_id,
                "character_id": selected_character_id
            },
            timeout=30
        )
        if response.status_code == 200:
            reply = response.json()["response"]
            logging.info(f"API response for thread_id='{thread_id}' | character_id='{selected_character_id}' | response='{reply[:50]}'")
            return reply
        else:
            error_detail = (
                response.json().get("detail", "Unknown error") 
                if response.headers.get("content-type") == "application/json" 
                else response.text
            )
            logging.error(f"API error {response.status_code} for thread_id='{thread_id}': {error_detail}")
            return f"Error: {response.status_code} - {error_detail}"
    except requests.exceptions.RequestException as e:
        logging.error(f"Connection error for thread_id='{thread_id}': {str(e)}")
        return f"Connection error: {str(e)}"

def load_thread_messages(thread_id: str):
    """Load messages for a thread from local storage."""
    if thread_id not in st.session_state.messages:
        st.session_state.messages[thread_id] = []
        logging.debug(f"Initialized message list for thread_id='{thread_id}'.")

def add_message_to_thread(thread_id: str, role: str, content: str):
    """Add a message to the current thread and log action."""
    if thread_id not in st.session_state.messages:
        st.session_state.messages[thread_id] = []
    st.session_state.messages[thread_id].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    logging.debug(
        f"Added message | thread_id='{thread_id}' | role='{role}' | content='{content[:50]}'"
    )

# === Sidebar for Thread Management ===
with st.sidebar:
    st.title("💬 Chat Threads")
    st.subheader("Select/Create Thread")
    thread_name = st.text_input("Thread Name", placeholder="Enter thread name...")

    if st.button("🔄 Load/Create Thread", type="primary"):
        if thread_name.strip():
            thread_id = thread_name.strip()
            st.session_state.current_thread = thread_id
            st.session_state.threads.add(thread_id)
            load_thread_messages(thread_id)
            logging.info(f"Loaded/Created thread: '{thread_id}'")
            st.success(f"Loaded thread: {thread_name}")
            st.rerun()
        else:
            st.error("Please enter a thread name")

    st.divider()
    st.subheader("Recent Threads")
    if st.session_state.threads:
        for thread_id in sorted(st.session_state.threads):
            message_count = len(st.session_state.messages.get(thread_id, []))
            button_label = f"📝 {thread_id} ({message_count} msgs)"
            if st.button(button_label, key=f"btn_{thread_id}"):
                st.session_state.current_thread = thread_id
                load_thread_messages(thread_id)
                logging.info(f"Switched to thread: '{thread_id}'")
                st.rerun()
    else:
        st.info("No threads yet. Create your first thread!")

    if st.session_state.threads:
        st.divider()
        if st.button("🗑️ Clear All Threads", type="secondary"):
            if st.button("⚠️ Confirm Clear All", type="secondary"):
                logging.warning(f"Clearing all threads & messages.")
                st.session_state.threads = set()
                st.session_state.messages = {}
                st.session_state.current_thread = None
                st.success("All threads cleared!")
                st.rerun()

# === Main Area ===
st.title("🤖 MPD Chatbot")

if st.session_state.current_thread:
    message_count = len(st.session_state.messages.get(st.session_state.current_thread, []))
    st.info(f"💬 Current Thread: **{st.session_state.current_thread}** | Messages: {message_count}")
else:
    st.warning("👈 Please enter a thread name and click 'Load/Create Thread' to start chatting")

# === Chat Messages Display ===
if st.session_state.current_thread:
    messages = st.session_state.messages.get(st.session_state.current_thread, [])
    for message in messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])

# === Chat Input ===
if st.session_state.current_thread:
    if prompt := st.chat_input("Type your message here..."):
        add_message_to_thread(st.session_state.current_thread, "user", prompt)
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message_to_api(prompt, st.session_state.current_thread)
                st.write(response)
        add_message_to_thread(st.session_state.current_thread, "assistant", response)
        st.rerun()
else:
    st.chat_input("Please select a thread first...", disabled=True)

# === Footer ===
st.divider()
st.caption("🚀 MPD Chatbot - Built with Streamlit & FastAPI")

