from models.gemini import llm

def chatbot_node(state):

    response = llm.invoke(
        f"""
        You are an agriculture expert.

        {state['query']}
        """
    )

    return {
        "answer":response.content
    }