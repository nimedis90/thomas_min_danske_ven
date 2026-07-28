"""
utils/ui_components.py
Componenti visivi per il rendering delle risposte del Tutor.
"""

import streamlit as st
from utils.translations import FLAG_MAP

def parse_gemini_response(raw_text: str) -> tuple[str, str, str]:
    """Scompone il testo grezzo di Gemini nelle 3 sezioni."""
    feedback, target_text, native_text = "", "", ""

    if "### FEEDBACK" in raw_text and "### NEWS_TARGET" in raw_text:
        parts = raw_text.split("### ")
        for part in parts:
            if part.startswith("FEEDBACK"):
                feedback = part.replace("FEEDBACK", "").strip()
            elif part.startswith("NEWS_TARGET"):
                target_text = part.replace("NEWS_TARGET", "").strip()
            elif part.startswith("NEWS_NATIVE"):
                native_text = part.replace("NEWS_NATIVE", "").strip()
    else:
        target_text = raw_text

    return feedback, target_text, native_text

def render_assistant_message(raw_text: str, native_lang: str, target_lang: str, ui: dict):
    """Renderizza il messaggio dell'assistente dividendo feedback e schede di traduzione."""
    feedback, target_text, native_text = parse_gemini_response(raw_text)

    flag_native = FLAG_MAP.get(native_lang, "🌐")
    flag_target = FLAG_MAP.get(target_lang, "🌐")

    # 1. Feedback grammaticale
    if feedback:
        st.markdown(f"{ui['feedback_header']}\n\n{feedback}")
        st.markdown("---")

    # 2. Tab con le Bandiere per la Notizia
    if target_text:
        tab_target_label = ui["original_tab"].format(flag=flag_target, lang=target_lang)
        tab_native_label = ui["translation_tab"].format(flag=flag_native, lang=native_lang)
        
        tab_target, tab_native = st.tabs([tab_target_label, tab_native_label])

        with tab_target:
            st.markdown(target_text)

        with tab_native:
            if native_text:
                st.markdown(f"{ui['translation_support']}\n\n{native_text}")
            else:
                st.info("Translation not available.")