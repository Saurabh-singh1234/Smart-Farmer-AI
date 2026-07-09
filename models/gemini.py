# cspell:ignore dotenv, genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# Import-time safety: different LangChain installs use different package names.
# Provide a clear error only when the model is actually used.
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception as e:  # pragma: no cover
    ChatGoogleGenerativeAI = None
    _import_error = e
else:
    _import_error = None


def _build_llm():
    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "Missing GOOGLE_API_KEY or GEMINI_API_KEY in environment. Add it to your .env file."
        )
    if ChatGoogleGenerativeAI is None:
        raise ModuleNotFoundError(
            "langchain_google_genai is not installed in this environment. "
            "Install it (or adjust requirements.txt) to use Gemini. "
            f"Original import error: {_import_error}"
        )

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.7,
    )


# Lazily built LLM instance.
# If Gemini dependencies are missing, keep import-time safe so the rest of the app can start.
try:
    llm = _build_llm()
except Exception:  # pragma: no cover
    llm = None



