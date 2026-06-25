from langgraph.graph import StateGraph

# Ensure repo root is on PYTHONPATH when imported from Streamlit
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.state import FarmerState
from agents.nodes import chatbot_node

builder = StateGraph(FarmerState)

builder.add_node(
    "chatbot",
    chatbot_node
)

builder.set_entry_point(
    "chatbot"
)

builder.set_finish_point(
    "chatbot"
)

graph = builder.compile()