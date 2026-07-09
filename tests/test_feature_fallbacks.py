import unittest
from io import BytesIO
from PIL import Image

from agents.nodes import chatbot_node
from tools.disease_tool import analyze_crop_image
from app import _append_unique_message


class FeatureFallbackTests(unittest.TestCase):
    def test_chatbot_node_returns_helpful_answer_when_model_fails(self):
        result = chatbot_node({"query": "How do I protect tomato plants?", "answer": ""})
        self.assertIn("answer", result)
        self.assertTrue(result["answer"].strip())

    def test_disease_analysis_returns_text_for_uploaded_image(self):
        image = Image.new("RGB", (200, 200), color=(120, 80, 40))
        buf = BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        pil_image = Image.open(buf)

        result = analyze_crop_image(pil_image)
        self.assertIsInstance(result, str)
        self.assertTrue(result.strip())

    def test_chatbot_node_gives_topic_specific_fallback(self):
        result = chatbot_node({"query": "How do I control leaf blight on tomato plants?", "answer": ""})
        answer = result["answer"].lower()
        self.assertTrue(any(word in answer for word in ["tomato", "blight", "leaf", "disease", "fungus"]))

    def test_chatbot_node_handles_yield_questions(self):
        result = chatbot_node({"query": "How can I increase crop yield in my field?", "answer": ""})
        answer = result["answer"].lower()
        self.assertTrue(any(word in answer for word in ["yield", "increase", "crop", "field", "growth"]))

    def test_duplicate_messages_are_not_appended(self):
        state = {"chat_messages": []}
        _append_unique_message(state, "chat_messages", {"role": "assistant", "content": "hello"})
        _append_unique_message(state, "chat_messages", {"role": "assistant", "content": "hello"})
        self.assertEqual(len(state["chat_messages"]), 1)


if __name__ == "__main__":
    unittest.main()
