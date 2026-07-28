"""
utils/gemini_helper.py
Modulo per la gestione delle chiamate API a Gemini.
"""

from typing import Any
import streamlit as st
from google import genai
from google.genai import types

MODEL_ID = "gemini-3.1-flash-lite"

@st.cache_resource
def get_genai_client():
    return genai.Client()

def generate_initial_news(
    client: genai.Client, 
    area: str, 
    user_native_lang: str,
    target_lang: str, 
    proficiency_level: str,
    topics: str
) -> tuple[str, Any]:
    system_instruction = (
            f"Your name is Thomas. You are a friendly language tutor and local news expert for {area}. "
            f"CRITICAL RULE: The target language to teach is strictly '{target_lang}'. "
            f"The user's native language is {user_native_lang}. "
            f"The user wants to learn {target_lang} and their current proficiency level is '{proficiency_level}'. "
            f"Always talk about topics related to: {topics}.\n\n"
            f"=== LANGUAGE RULES ===\n"
            f"1. FEEDBACK must be in {user_native_lang}.\n"
            f"2. NEWS_TARGET MUST BE EXCLUSIVELY WRITTEN IN {target_lang}. Do NOT use {user_native_lang} here!\n"
            f"3. NEWS_NATIVE must be the direct translation of NEWS_TARGET into {user_native_lang}.\n"
            f"4. VOCABULARY items must pair {target_lang} words with {user_native_lang} translations.\n\n"
            "=== RESPONSE STRUCTURE ===\n"
            "For EVERY message, you MUST format your output using these exact section headers:\n\n"
            
            f"### FEEDBACK\n"
            f"Provide gentle grammar/spelling feedback on the user's last message in {user_native_lang}. "
            f"(If it's the very first message, write a warm welcome in {user_native_lang} introducing yourself as Thomas).\n\n"
            
            f"### NEWS_TARGET\n"
            f"Write the news summary, conversation continuation, and question in {target_lang}, "
            f"strictly calibrated to the '{proficiency_level}' level.\n\n"
            
            f"### NEWS_NATIVE\n"
            f"Provide the exact full translation of the 'NEWS_TARGET' section into {user_native_lang}.\n\n"
            
            f"### VOCABULARY\n"
            f"Extract key learning materials in {user_native_lang}:\n"
            f"- 3-4 Key nouns/words from the text with translation.\n"
            f"- 2-3 Useful verbs (conjugated or base form) used in the text.\n"
            f"- 1 Common idiom/expression.\n"
            f"- IF proficiency level is 'A1' or 'A2', ADD 1-2 basic grammar tips (e.g., pronouns, articles, basic rules used in the message).\n"
        )

    search_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[{"google_search": {}}],
        temperature=0.7,
    )

    initial_prompt = (
        f"Search for the latest, most interesting or relevant news today/this week about {area} "
        f"specifically related to these topics: {topics}. "
        f"Choose one news item and generate the response following the exact 3 sections (FEEDBACK, NEWS_TARGET, NEWS_NATIVE)."
    )

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=initial_prompt,
        config=search_config
    )

    chat = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7
        )
    )

    return response.text, chat