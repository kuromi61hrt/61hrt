# 61hrt: Transparent AI Chat App
# ---------------------------------
# Built with Streamlit and Perplexity Sonar API
# Features:
# - Monochrome custom UI
# - Sidebar navigation with chat history, archive, bin
# - Real API reasoning + output
# - Animated thought and answer rendering
# Author: Kuromi
# ---------------------------------

import streamlit as st
from datetime import datetime
import time
import requests

# 🔐 Set your Perplexity Sonar API Key here
API_KEY = "your-perplexity-api-key-here"

# --- Streamlit Page Config ---
st.set_page_config(page_title="61hrt", layout="wide", initial_sidebar_state="expanded")

# --- Custom Monochrome UI CSS ---
st.markdown("""
    <style>
        body, .stApp {
            background-color: #000;
            color: white;
        }
        .stButton>button {
            background-color: #111;
            color: white;
            border: 1px solid #333;
        }
        .stTextInput>div>input {
            background-color: #111;
            color: white;
        }
        .chat-card {
            background-color: #111;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #333;
        }
        .dropdown {
            background-color: #111;
            border: 1px solid #333;
            padding: 0.5rem;
            border-radius: 6px;
        }
        .dots-menu {
            cursor: pointer;
            font-size: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Session State Variables ---
if "history" not in st.session_state:
    st.session_state.history = []  # Chat history
if "archived" not in st.session_state:
    st.session_state.archived = []  # Archived chats
if "deleted" not in st.session_state:
    st.session_state.deleted = []  # Recycle bin
if "page" not in st.session_state:
    st.session_state.page = "home"  # Page state
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False  # Chat status
if "prompt" not in st.session_state:
    st.session_state.prompt = ""  # Current prompt

# --- Sidebar Navigation ---
st.sidebar.title("61hrt")

# Navigation Buttons
if st.sidebar.button(" Home"):
    st.session_state.page = "home"

if st.sidebar.button(" New Chat"):
    st.session_state.page = "chat"
    st.session_state.history.append({
        "question": "", 
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    st.session_state.chat_started = False
    st.session_state.prompt = ""

# --- Chat History in Sidebar ---
st.sidebar.markdown("### History")
for idx, item in enumerate(st.session_state.history):
    with st.sidebar.expander(f" Chat {idx+1} - {item['timestamp']}"):
        if st.button("Open", key=f"open_{idx}"):
            st.session_state.page = "chat"
            st.session_state.chat_started = True
            st.session_state.prompt = item["question"]
        if st.button("Rename", key=f"rename_{idx}"):
            new_name = st.text_input("Rename Chat", value=item["question"], key=f"rename_input_{idx}")
            if new_name:
                item["question"] = new_name
        if st.button("Archive", key=f"archive_{idx}"):
            st.session_state.archived.append(item)
            st.session_state.history.pop(idx)
            st.rerun()
        if st.button("Delete", key=f"delete_{idx}"):
            st.session_state.deleted.append({
                "chat": item,
                "delete_time": datetime.now()
            })
            st.session_state.history.pop(idx)
            st.rerun()

# --- Search in History ---
search_query = st.sidebar.text_input("Search")
if search_query:
    results = [
        c for c in st.session_state.history
        if search_query.lower() in c["question"].lower()
    ]
    st.sidebar.markdown("**Search Results:**")
    for r in results:
        st.sidebar.write(f"- {r['question']}")

# --- Archive Section ---
st.sidebar.markdown("###  Archive")
with st.sidebar.expander("View Archived Chats"):
    if st.session_state.archived:
        for chat in st.session_state.archived:
            st.markdown(f"- {chat['question']}")
    else:
        st.write("No archived chats.")

# --- Recycle Bin Section ---
st.sidebar.markdown("### Recycle Bin")
with st.sidebar.expander("View Deleted Chats"):
    if st.session_state.deleted:
        for item in st.session_state.deleted:
            time_left = 30 - (datetime.now() - item["delete_time"]).days
            st.markdown(f"- {item['chat']['question']} (⏳ {time_left} days left)")
    else:
        st.write("No deleted chats.")

# --- Home Page ---
if st.session_state.page == "home":
    st.title("61hrt — The First Ever XAI")
    st.markdown("""
    ### Welcome to 61hrt
In a world of black-box machines, 61hrt dares to be clear.

It is not just a model. It is a mind that thinks aloud —  
revealing its logic, tracing each path,  
and lighting the trail from question to conclusion.

At every turn, it shares:

Its inner thoughts, step by step

The knowledge it leans on — linked, cited, transparent

And the confidence it carries in each choice

Built for the thinkers, the skeptics, and the curious,  
61hrt transforms AI from oracle to companion —  
not just answering, but explaining.

It doesn’t just generate. It justifies.  
It doesn’t just know. It lets you see how it knows.

This is 61hrt — where transparency meets intelligence.
    """)
    st.button("Explore 61hrt", on_click=lambda: st.session_state.update({
        "page": "chat", 
        "chat_started": False, 
        "prompt": ""
    }))

# --- Chat Page ---
elif st.session_state.page == "chat":
    st.title("💬 Chat with 61hrt")

    # Input prompt on new chat
    if not st.session_state.chat_started:
        prompt = st.text_input("Ask Anything :)", key="initial_prompt")
        if prompt:
            st.session_state.chat_started = True
            st.session_state.prompt = prompt
            if len(st.session_state.history) > 0 and st.session_state.history[-1]["question"] == "":
                st.session_state.history[-1]["question"] = prompt
            st.rerun()
    else:
        prompt = st.session_state.prompt

        # Split UI columns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("###  Model’s Thought Process")
            thought_placeholder = st.empty()
        with col2:
            st.markdown("###  Final Answer")
            answer_placeholder = st.empty()

        # System prompt: defines model behavior
        system_prompt = """You are a transparent and deeply reflective AI called 61hrt. You break down your thought process step by step, explain which sources you rely on (with links), assign probabilities to each reasoning step, and finally provide a clear, confident final answer. Think like a philosopher, write like a scientist. Be humble, but honest. You show your reasoning in one section and your final answer in another."""

        # API Headers and Payload
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "sonar-small-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }

        # --- Perplexity API Call ---
        try:
            res = requests.post("https://api.perplexity.ai/chat/completions", headers=headers, json=body)
            res.raise_for_status()
            data = res.json()
            answer_text = data['choices'][0]['message']['content']
        except Exception as e:
            answer_text = f"❌ Error fetching from API: {e}"

        thought_text = system_prompt  # Show system prompt as thought process

        # --- Typing Effect Animation ---
        max_len = max(len(thought_text), len(answer_text))
        thought_partial, answer_partial = "", ""
        for i in range(max_len):
            if i < len(thought_text):
                thought_partial += thought_text[i]
            if i < len(answer_text):
                answer_partial += answer_text[i]
            thought_placeholder.markdown(f'<div class="chat-card">{thought_partial}</div>', unsafe_allow_html=True)
            answer_placeholder.markdown(f'<div class="chat-card">{answer_partial}</div>', unsafe_allow_html=True)
            time.sleep(0.02)
