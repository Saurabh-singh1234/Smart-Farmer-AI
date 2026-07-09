# cspell:ignore biofertilizer neem overwatering
from models.gemini import llm


def _fallback_agriculture_reply(query: str) -> str:
    question = (query or "").strip().lower()
    crop_names = ["tomato", "potato", "wheat", "rice", "corn", "cotton", "paddy", "apple", "banana", "mango"]
    matched_crop = next((crop for crop in crop_names if crop in question), None)

    if any(word in question for word in ["organic farming", "organic", "compost", "biofertilizer", "natural farming"]):
        return (
            "Organic farming is a way of growing crops without synthetic chemical fertilizers or pesticides.\n\n"
            "Step 1: Build soil health with compost, farmyard manure, and cover crops.\n"
            "Step 2: Rotate crops so pests and diseases do not build up in the same field.\n"
            "Step 3: Use natural pest control such as neem, beneficial insects, and hand removal where possible.\n"
            "Step 4: Mulch the soil to conserve moisture and reduce weeds.\n\n"
            "Why it helps: this approach improves soil fertility, protects the environment, and produces safer food over time."
        )

    if any(word in question for word in ["yield", "increase", "boost", "more production", "production", "harvest"]):
        return (
            "To increase crop yield, follow these steps:\n\n"
            "Step 1: Use healthy, certified seeds and plant them at the correct spacing.\n"
            "Step 2: Test the soil and apply balanced fertilizer only where needed.\n"
            "Step 3: Water regularly but avoid overwatering and waterlogging.\n"
            "Step 4: Remove weeds early and inspect the crop for pests or disease.\n"
            "Step 5: Harvest at the right time so the produce is full and healthy.\n\n"
            "Why it helps: better spacing, proper nutrition, and regular monitoring usually improve both the amount and quality of the harvest."
        )

    if any(word in question for word in ["disease", "pest", "leaf", "fungus", "mold", "blight", "spot", "rot"]):
        crop_hint = f" for {matched_crop}" if matched_crop else ""
        return (
            f"For crop disease issues{crop_hint}, follow this plan:\n\n"
            "Step 1: Inspect the leaves, stems, and roots carefully to identify the problem.\n"
            "Step 2: Remove badly infected leaves or plants so the disease does not spread.\n"
            "Step 3: Improve airflow and avoid overwatering.\n"
            "Step 4: Keep the field clean and remove weeds or fallen debris.\n"
            "Step 5: If the problem continues, contact a local agriculture expert for a stronger treatment suggestion.\n\n"
            "Why it helps: early action prevents the disease from spreading to healthy plants."
        )

    if any(word in question for word in ["fertilizer", "nutrient", "soil", "manure", "growth"]):
        return (
            "For soil and fertilizer questions, use this approach:\n\n"
            "Step 1: Do a soil test before adding fertilizer.\n"
            "Step 2: Apply nutrients only if the crop shows a clear deficiency.\n"
            "Step 3: Use balanced fertilizer and avoid excess amounts.\n"
            "Step 4: Add compost or organic manure to improve long-term soil health.\n"
            "Step 5: Rotate crops to keep the soil productive.\n\n"
            "Why it helps: balanced nutrition supports healthy growth without damaging the soil."
        )

    if any(word in question for word in ["water", "irrigation", "dry", "moisture"]):
        return (
            "For irrigation, follow these steps:\n\n"
            "Step 1: Check the soil moisture before watering.\n"
            "Step 2: Water deeply but not too often so roots grow strong.\n"
            "Step 3: Water early in the morning to reduce evaporation.\n"
            "Step 4: Avoid wetting leaves late in the day.\n"
            "Step 5: Adjust the schedule based on weather and crop stage.\n\n"
            "Why it helps: good irrigation improves root growth and reduces water stress."
        )

    if any(word in question for word in ["care", "healthy", "plant", "crop", "field", "farm"]):
        return (
            "For healthy crop growth, use this simple plan:\n\n"
            "Step 1: Keep the field weed-free and clean.\n"
            "Step 2: Check soil moisture and water only when needed.\n"
            "Step 3: Provide balanced nutrition through soil management or fertilizer.\n"
            "Step 4: Inspect leaves and stems regularly for pests or disease.\n"
            "Step 5: Remove weak plants and rotate crops when possible.\n\n"
            "Why it helps: regular care keeps crops strong and reduces losses."
        )

    if matched_crop:
        return (
            f"For {matched_crop}, use this step-by-step approach:\n\n"
            f"Step 1: Check the leaves, soil, and roots regularly for any change.\n"
            f"Step 2: Keep watering balanced and avoid water stress.\n"
            f"Step 3: Remove weeds and keep the area clean.\n"
            f"Step 4: Watch for discoloration, spots, or weak growth.\n"
            f"Step 5: Act quickly if you notice any unusual symptoms.\n\n"
            "Why it helps: early attention prevents small issues from becoming serious crop losses."
        )

    return (
        "I can help with crop care, disease detection, irrigation, soil health, and fertilizer advice. Ask me a specific question about your farm and I will guide you step by step."
    )


def chatbot_node(state):
    query = state.get("query", "") if isinstance(state, dict) else str(state)
    query = str(query).strip()

    if not query:
        return {"answer": "How can I help with your farm today?"}

    if llm is None:
        return {"answer": _fallback_agriculture_reply(query)}

    try:
        response = llm.invoke(
            f"""
            You are a practical agriculture assistant.
            Answer in a concise, helpful way for a farmer.

            User question: {query}
            """
        )
        content = getattr(response, "content", None)
        if content:
            return {"answer": str(content).strip()}
    except Exception:
        pass

    return {"answer": _fallback_agriculture_reply(query)}

