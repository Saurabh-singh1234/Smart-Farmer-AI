import os
import uuid

import numpy as np
import sounddevice as sd
import speech_recognition as sr
from gtts import gTTS


def speech_to_text(
    language: str = "en-IN",
    phrase_time_limit: int = 10,
    sample_rate: int = 16000,
):
    """Capture microphone audio and recognize speech.

    Returns:
        str: recognized text

    Raises:
        RuntimeError: for user-facing actionable errors.
    """
    recognizer = sr.Recognizer()

    try:
        recording = sd.rec(
            int(phrase_time_limit * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float64",
        )
        sd.wait()

        int_data = (recording * 32767).astype(np.int16)
        raw_bytes = int_data.tobytes()

        audio = sr.AudioData(raw_bytes, sample_rate, 2)
    except Exception as e:
        raise RuntimeError(
            "Microphone not available or audio capture failed. "
            "Ensure you have a working mic."
        ) from e

    try:
        text = recognizer.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError as e:
        raise RuntimeError("Could not understand the speech. Please try again with clearer audio.") from e
    except sr.RequestError as e:
        raise RuntimeError(
            "Speech recognition request failed (likely no internet or Google endpoint blocked)."
        ) from e
    except Exception as e:
        raise RuntimeError(f"Speech recognition failed: {e}") from e


def text_to_voice(text: str, lang: str = "en"):
    """Convert text to speech using gTTS.

    Returns:
        str: path to the saved MP3 file.
    """
    if text is None:
        raise RuntimeError("No text provided for speech synthesis.")

    text = str(text).strip()
    if not text:
        raise RuntimeError("Empty text provided for speech synthesis.")

    # Save per-call to avoid collisions when Streamlit reruns.
    filename = f"response_{uuid.uuid4().hex}.mp3"
    path = os.path.abspath(filename)

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(path)
    except Exception as e:
        raise RuntimeError(f"Text-to-speech failed: {e}") from e

    return path

