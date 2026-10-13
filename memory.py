
def add_message(history, role, content):
    """Add a message to the conversation history."""
    history.append({
        "role": role,
        "content": content
    })


def get_recent_history(history, max_turns=5):
    """
    Return the most recent complete conversation turns.
    Each completed turn contains a user and assistant message.
    """
    max_messages = max_turns * 2
    return history[-max_messages:]


def clear_history():
    """Return an empty conversation history."""
    return []
