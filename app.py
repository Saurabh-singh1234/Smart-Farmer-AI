import os
import sys
from pathlib import Path

# Ensure repo root is on PYTHONPATH so `import models...` works when Streamlit runs
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import streamlit as st
from agents.graph import graph
from services.speech_service import (
    speech_to_text,
    text_to_voice
)
from tools.disease_tool import analyze_crop_image
from PIL import Image

st.set_page_config(
    page_title="Smart Farmer AI",
    layout="wide"
)

st.title("🌾 Smart Farmer Assistant")

# Keep chat history separate from voice interactions.
if "chat_messages" not in st.session_state:
    existing_chat = st.session_state.pop("messages", [])
    st.session_state.chat_messages = existing_chat

if "voice_last_question" not in st.session_state:
    st.session_state.voice_last_question = ""

if "voice_last_answer" not in st.session_state:
    st.session_state.voice_last_answer = ""


def _extract_answer(result):
    if isinstance(result, dict):
        return (
            result.get("answer")
            or result.get("response")
            or result.get("result")
            or str(result)
        )
    return str(result)


def _append_unique_message(state, key, message):
    messages = state.setdefault(key, [])
    if not messages:
        messages.append(message)
        return

    last_message = messages[-1]
    if last_message.get("role") == message.get("role") and last_message.get("content") == message.get("content"):
        return

    messages.append(message)


# Tabs
tab1, tab2, tab3 = st.tabs(
    [
        "Chat",
        "Voice",
        "Disease Detection"
    ]
)

# =========================
# CHAT TAB
# =========================
with tab1:

    st.subheader("💬 Chat Assistant")
    st.caption("Type your question once; the answer will appear below.")

    with st.form("chat_form", clear_on_submit=True):
        question = st.text_input("Ask anything...", key="chat_question_input")
        submitted = st.form_submit_button("Send")

    if submitted:
        if not question or not str(question).strip():
            st.warning("Please enter a question first.")
        else:
            question = str(question).strip()

            _append_unique_message(
                st.session_state,
                "chat_messages",
                {
                    "role": "user",
                    "content": question
                }
            )

            chat_answer = None
            chat_result = None
            try:
                chat_result = graph.invoke(
                    {
                        "query": question,
                        "answer": ""
                    }
                )
            except Exception as e:
                st.error(f"Chat failed: {e}")
                chat_answer = "I could not reach the AI service right now, but I can still help with general farming advice."

            if chat_answer is None and chat_result is not None:
                chat_answer = _extract_answer(chat_result)

            _append_unique_message(
                st.session_state,
                "chat_messages",
                {
                    "role": "assistant",
                    "content": chat_answer
                }
            )

    st.markdown("---")
    if st.session_state.chat_messages:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(f"<div style='font-size: 1.05rem; line-height: 1.6;'>{msg['content']}</div>", unsafe_allow_html=True)

# =========================
# VOICE TAB
# =========================
with tab2:

    st.subheader("🎤 Voice Assistant")

    st.caption("Speak your farming question and hear the answer back.")

    if st.button(
        "🎙️ Ask by Voice",
        key="voice_btn"
    ):
        st.info("Speak now...")

        try:
            raw_voice_text = speech_to_text()
        except Exception as e:
            st.warning(f"Voice capture unavailable: {e}")
            raw_voice_text = None

        voice_question = raw_voice_text.strip() if isinstance(raw_voice_text, str) else ""

        if not voice_question:
            st.error("Could not recognize speech. Please try again.")
        else:
            st.success(f"You said: {voice_question}")

            try:
                voice_result = graph.invoke(
                    {
                        "query": voice_question,
                        "answer": ""
                    }
                )
            except Exception as e:
                st.error(f"Voice query failed: {e}")
                voice_answer = "I could not reach the AI service right now, but I can still help with general farming advice."
            else:
                voice_answer = _extract_answer(voice_result)

            st.session_state.voice_last_question = voice_question
            st.session_state.voice_last_answer = voice_answer

            st.write("### AI Response")
            st.markdown(f"<div style='font-size: 1.08rem; line-height: 1.7;'>{voice_answer}</div>", unsafe_allow_html=True)

            audio_file = text_to_voice(voice_answer)
            st.audio(audio_file)

# =========================
# DISEASE DETECTION TAB
# =========================
with tab3:

    st.subheader("🌿 Crop Disease Detection")

    uploaded_file = st.file_uploader(
        "Upload Crop Image",
        type=["jpg", "jpeg", "png"]
    )

    if st.button(
        "Detect Disease",
        key="disease_btn"
    ):

        if uploaded_file is None:
            st.warning(
                "⚠️ Please upload an image first."
            )

        else:

            image = Image.open(uploaded_file)

            st.image(
                image,
                caption="Uploaded Image",
                use_container_width=True
            )

            try:
                disease_result = analyze_crop_image(image)

                st.write("### Disease Analysis")
                st.markdown(f"<div style='font-size: 1.08rem; line-height: 1.7;'>{disease_result}</div>", unsafe_allow_html=True)

                audio_file = text_to_voice(disease_result)
                st.audio(audio_file)
            except Exception as e:
                st.error(f"Disease detection failed: {e}")
