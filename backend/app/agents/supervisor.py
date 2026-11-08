def supervisor_node(state: dict) -> dict:
    message = state["user_message"].lower()

    # Lead generation and appointment-related intents
    lead_keywords = [
        "buy",
        "buying",
        "interested",
        "purchase",
        "visit",
        "schedule",
        "appointment",
        "book",
        "booking",
        "contact",
        "call me",
        "talk to sales",
    ]

    # Property information intents
    knowledge_keywords = [
        "price",
        "property",
        "apartment",
        "bedroom",
        "location",
        "amenities",
        "facilities",
        "configuration",
        "area",
    ]

    # Give lead-generation intents priority
    if any(keyword in message for keyword in lead_keywords):
        agent = "lead"
        intent = "lead_generation"

    elif any(keyword in message for keyword in knowledge_keywords):
        agent = "knowledge"
        intent = "property_information"

    else:
        agent = "knowledge"
        intent = "general_information"

    return {
        "selected_agent": agent,
        "intent": intent,
        "next_step": agent,
    }