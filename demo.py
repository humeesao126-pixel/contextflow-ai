
# -----------------------------------
# ContextFlow AI - Offline Demo Engine
# -----------------------------------

def generate_demo_response(prompt):
    """
    Generate simulated responses for local testing.
    No internet or Gemini API required.
    """

    text = prompt.lower().strip()

    if "python" in text:
        return (
            "🧪 [DEMO RESPONSE]\n\n"
            "Python is a beginner-friendly programming "
            "language used for web development, "
            "automation, data science, and AI."
        )

    if "mars" in text:
        return (
            "🧪 [DEMO RESPONSE]\n\n"
            "Mars is the fourth planet from the Sun. "
            "It is commonly known as the Red Planet."
        )

    if "memory" in text:
        return (
            "🧪 [DEMO RESPONSE]\n\n"
            "ContextFlow AI uses conversation history "
            "to maintain context. This response is "
            "simulated for development testing."
        )

    return (
        "🧪 [DEMO RESPONSE]\n\n"
        f"Your message was received: {prompt}\n\n"
        "This is a simulated response used to test "
        "the application's features without the API."
    )
