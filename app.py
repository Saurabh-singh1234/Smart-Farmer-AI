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

# Chat messages only
if "messages" not in st.session_state:
    st.session_state.messages = []

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

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if (question := st.chat_input("Ask anything...")):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        chat_result = graph.invoke(
            {
                "query": question,
                "answer": ""
            }
        )


        if isinstance(chat_result, dict):
            chat_answer = (
                chat_result.get("answer")
                or chat_result.get("response")
                or chat_result.get("result")
                or str(chat_result)
            )
        else:

            chat_answer = str(chat_result)

        # Keep streamlit session state in sync and match FarmerState shape
        # (helps static type checkers; LangGraph runtime doesn't require this assignment)
        # chat_result should always include "answer"; fallback ensures output exists.


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": chat_answer
            }
        )

        with st.chat_message("assistant"):
            st.write(chat_answer)

# =========================
# VOICE TAB
# =========================
with tab2:

    st.subheader("🎤 Voice Assistant")

    if st.button(
        "🎙️ Ask by Voice",
        key="voice_btn"
    ):

        st.info("Speak now...")

        raw_voice_text = speech_to_text()
        voice_question = raw_voice_text.strip() if isinstance(raw_voice_text, str) else ""

        if not voice_question:
            st.error("Could not recognize speech")

        else:

            st.success(
                f"You said: {voice_question}"
            )

            voice_result = graph.invoke(
                {
                    "query": voice_question,
                    "answer": ""
                }
            )


            if isinstance(voice_result, dict):
                voice_answer = (
                    voice_result.get("answer")
                    or voice_result.get("response")
                    or voice_result.get("result")
                    or str(voice_result)
                )
            else:
                voice_answer = str(voice_result)

            st.write("### AI Response")
            st.write(voice_answer)

            audio_file = text_to_voice(
                voice_answer
            )

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

            disease_result = analyze_crop_image(
                image
            )

            st.write("### Disease Analysis")
            st.write(disease_result)

            audio_file = text_to_voice(
                disease_result
            )

            st.audio(audio_file)