import streamlit as st
import requests
import json
from datetime import datetime
from typing import List, Dict

# Configure the page
st.set_page_config(
    page_title="MPD Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
# API_BASE_URL = "http://localhost:8000"  # For local development
# Use Docker service name for production

API_BASE_URL = "http://api:8000"  # Docker service name

# Initialize session state
if "current_thread" not in st.session_state:
    st.session_state.current_thread = None
if "threads" not in st.session_state:
    st.session_state.threads = set()  # Just store thread names
if "messages" not in st.session_state:
    st.session_state.messages = {}

def send_message_to_api(message: str, thread_id: str) -> str:
    """Send message to the FastAPI backend"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={
                "message": message,
                "thread_id": thread_id
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            error_detail = response.json().get("detail", "Unknown error") if response.headers.get("content-type") == "application/json" else response.text
            return f"Error: {response.status_code} - {error_detail}"
    except requests.exceptions.RequestException as e:
        return f"Connection error: {str(e)}"

def load_thread_messages(thread_id: str):
    """Load messages for a thread from local storage"""
    if thread_id not in st.session_state.messages:
        st.session_state.messages[thread_id] = []

def add_message_to_thread(thread_id: str, role: str, content: str):
    """Add a message to the current thread"""
    if thread_id not in st.session_state.messages:
        st.session_state.messages[thread_id] = []
    
    st.session_state.messages[thread_id].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })

# Sidebar for thread management
with st.sidebar:
    st.title("💬 Chat Threads")
    
    # Create new thread section
    st.subheader("Select/Create Thread")
    thread_name = st.text_input("Thread Name", placeholder="Enter thread name...")
    
    if st.button("🔄 Load/Create Thread", type="primary"):
        if thread_name.strip():
            # Use the thread name directly as thread_id
            thread_id = thread_name.strip()
            st.session_state.current_thread = thread_id
            st.session_state.threads.add(thread_id)
            
            # Load existing messages for this thread
            load_thread_messages(thread_id)
            
            st.success(f"Loaded thread: {thread_name}")
            st.rerun()
        else:
            st.error("Please enter a thread name")
    
    st.divider()
    
    # Display existing threads
    st.subheader("Recent Threads")
    
    if st.session_state.threads:
        for thread_id in sorted(st.session_state.threads):
            message_count = len(st.session_state.messages.get(thread_id, []))
            button_label = f"📝 {thread_id} ({message_count} msgs)"
            
            if st.button(button_label, key=f"btn_{thread_id}"):
                st.session_state.current_thread = thread_id
                load_thread_messages(thread_id)
                st.rerun()
    else:
        st.info("No threads yet. Create your first thread!")
    
    # Clear all threads button
    if st.session_state.threads:
        st.divider()
        if st.button("🗑️ Clear All Threads", type="secondary"):
            if st.button("⚠️ Confirm Clear All", type="secondary"):
                st.session_state.threads = set()
                st.session_state.messages = {}
                st.session_state.current_thread = None
                st.success("All threads cleared!")
                st.rerun()

# Main chat area
st.title("🤖 MPD Chatbot")

# Display current thread info
if st.session_state.current_thread:
    message_count = len(st.session_state.messages.get(st.session_state.current_thread, []))
    st.info(f"💬 Current Thread: **{st.session_state.current_thread}** | Messages: {message_count}")
else:
    st.warning("👈 Please enter a thread name and click 'Load/Create Thread' to start chatting")

# Chat messages display
if st.session_state.current_thread:
    messages = st.session_state.messages.get(st.session_state.current_thread, [])
    
    # Display messages
    for message in messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])

# Chat input
if st.session_state.current_thread:
    # Use chat_input for better UX
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to thread
        add_message_to_thread(st.session_state.current_thread, "user", prompt)
        
        # Display user message immediately
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get response from API
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message_to_api(prompt, st.session_state.current_thread)
                st.write(response)
        
        # Add assistant response to thread
        add_message_to_thread(st.session_state.current_thread, "assistant", response)
        
        # Rerun to update the interface
        st.rerun()
else:
    st.chat_input("Please select a thread first...", disabled=True)

# Footer
st.divider()
st.caption("🚀 MPD Chatbot - Built with Streamlit & FastAPI")
