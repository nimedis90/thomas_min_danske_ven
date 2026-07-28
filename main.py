"""
main.py
Interfaccia Principale per Thomas - Language Tutor.
"""

import streamlit as st
from utils.gemini_helper import get_genai_client, generate_initial_news
from utils.translations import LANGUAGES_LIST, get_translation
from utils.ui_components import render_assistant_message

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Thomas - Language Tutor", page_icon="🧑‍🏫", layout="wide")

try:
    client = get_genai_client()
except Exception:
    st.error("Please ensure the GEMINI_API_KEY environment variable is set.")
    st.stop()

# --- SIDEBAR & INTERFACCIA DINAMICA ---
native_lang = st.sidebar.selectbox("1. Native Language / Lingua Madre:", LANGUAGES_LIST, index=0)
ui = get_translation(native_lang)

st.sidebar.title(ui["sidebar_profile"])
target_lang = st.sidebar.selectbox(ui["target_lang"], LANGUAGES_LIST, index=1)

levels = ["A1", "A2", "B1-B2", "C1-C2"]
selected_level = st.sidebar.select_slider(ui["level_label"], options=levels, value="A1")

st.sidebar.markdown("---")
st.sidebar.title(ui["sidebar_interests"])

target_area = st.sidebar.text_input(ui["location"], value="London")
selected_topics = st.sidebar.multiselect(ui["topics_label"], options=ui["preset_topics"], default=[ui["preset_topics"][0]])
custom_topic = st.sidebar.text_input(ui["custom_topic_label"], placeholder=ui["custom_topic_placeholder"])

all_topics = list(selected_topics) + ([custom_topic.strip()] if custom_topic.strip() else [])
topics_str = ", ".join(all_topics) if all_topics else "General News"

start_button = st.sidebar.button(ui["start_button"], use_container_width=True)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_instance" not in st.session_state:
    st.session_state.chat_instance = None

def init_session():
    st.session_state.messages = []
    with st.spinner(ui["searching_spinner"].format(area=target_area)):
        first_msg, chat_obj = generate_initial_news(
            client, target_area, native_lang, target_lang, selected_level, topics_str
        )
        st.session_state.chat_instance = chat_obj
        st.session_state.messages.append({"role": "assistant", "content": first_msg})

# --- VISTA PRINCIPALE ---
st.title(f"{ui['main_title']} {target_lang}")

if start_button and target_area.strip():
    init_session()

# Schermata di Benvenuto vs Chat Attiva
if st.session_state.chat_instance is None:
    st.info(ui["info_banner"])
    st.markdown(f"{ui['how_it_works_title']}\n{ui['step_1']}\n{ui['step_2']}\n{ui['step_3']}")
else:
    st.subheader(ui["location_header"].format(area=target_area, level=selected_level))
    st.caption(f"📌 **Focus:** {topics_str}")

    # Storico Chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(msg["content"])
            else:
                render_assistant_message(msg["content"], native_lang, target_lang, ui)

    # Input Utente
    if user_input := st.chat_input(ui["chat_placeholder"].format(target=target_lang)):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner(ui["analyzing_spinner"]):
                reply = st.session_state.chat_instance.send_message(user_input)
                render_assistant_message(reply.text, native_lang, target_lang, ui)
                st.session_state.messages.append({"role": "assistant", "content": reply.text})