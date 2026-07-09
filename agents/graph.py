# NOTE:
# LangGraph is optional for this repo.
# Your environment currently has dependency resolution issues around LangGraph
# (missing submodules like `langgraph.cache`). To keep the app runnable,
# we provide a tiny shim that mimics the `graph.invoke(payload)` API.

import sys
from pathlib import Path

# Ensure repo root is on PYTHONPATH when imported from Streamlit
REPO_ROOT = Path(__file__).resolve()
while REPO_ROOT != REPO_ROOT.parent:
    if (REPO_ROOT / "app.py").exists():
        break
    REPO_ROOT = REPO_ROOT.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.nodes import chatbot_node


class _GraphShim:
    """Minimal `graph.invoke` compatible object."""

    def invoke(self, payload: dict):
        # Payload shape comes from app.py:
        # {"query": question, "answer": ""}
        return chatbot_node(payload)


graph = _GraphShim()

