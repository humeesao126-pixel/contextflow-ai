import time
from demo import generate_demo_response
from datetime import datetime
from textwrap import dedent
import streamlit as st
from google import genai
from google.genai import types,errors

from memory import (
    add_message,
    get_recent_history,
    clear_history
)


from database import (
    initialize_database,
    create_conversation,
    save_message,
    save_exchange,
    load_messages,
    list_conversations,
    rename_conversation,
    delete_conversation
)

# -----------------------------------
# 1. Page configuration
# -----------------------------------
st.set_page_config(
    page_title="ContextFlow AI",
    page_icon="🧠",
    layout="centered"
)



# -----------------------------------
# Cloud Lilac Studio - Soft & Elegant UI
# -----------------------------------

st.markdown("""
<style>

/* Main application background */
[data-testid="stAppViewContainer"] {
    background: #F8F7FC;
    color: #342646;
}

/* Main content layout */
.block-container {
    max-width: 1000px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #F0EBF9;
    border-right: 1px solid #E4DCEC;
}

/* Sidebar text */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #45345F;
}

/* Application heading */
.app-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #5B438A;
    letter-spacing: -1px;
    margin-bottom: 0.3rem;
}

/* Application subtitle */
.app-subtitle {
    color: #81748F;
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* Chat message cards */
[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border: 1px solid #E8E2F0;
    border-radius: 18px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 4px 18px rgba(91, 67, 138, 0.04);
}

/* User chat messages */
[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) {
    background: #EDE5F8;
    border-color: #DDD0EF;
}

/* Buttons */
.stButton > button {
    background: #FFFFFF;
    color: #5B438A;
    border: 1px solid #DED3EC;
    border-radius: 12px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #EDE5F8;
    color: #49346F;
    border-color: #A88CCD;
    box-shadow: 0 4px 12px rgba(128, 104, 189, 0.12);
}

/* Input fields */
[data-testid="stChatInput"] {
    background: #FFFFFF;
    border: 1px solid #DED3EC;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(91, 67, 138, 0.06);
}

/* Expanders */
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid #E4DCEC;
    border-radius: 12px;
}

/* Sidebar separators */
[data-testid="stSidebar"] hr {
    border-color: #E0D6EB;
}

/* Subtle transitions */
button, input, textarea {
    transition: all 0.2s ease;
}


/* -----------------------------------
   Cloud Lilac Welcome Panel
----------------------------------- */

.cloud-welcome {
    background: linear-gradient(120deg, #FFFFFF, #F5EFFC);
    border: 1px solid #E8E2F0;
    border-radius: 22px;
    padding: 32px 36px;
    margin-top: 10px;
    margin-bottom: 24px;
    box-shadow: 0 8px 28px rgba(91, 67, 138, 0.06);
}

.cloud-eyebrow {
    color: #8068BD;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.6px;
    margin-bottom: 12px;
}

.cloud-welcome h1 {
    color: #342646;
    font-size: 2.2rem;
    font-weight: 750;
    letter-spacing: -0.8px;
    margin: 0 0 12px 0;
}

.cloud-welcome p {
    color: #81748F;
    font-size: 1rem;
    line-height: 1.6;
    margin: 0;
}

/* Suggested prompts heading */
.cloud-suggestions {
    color: #8B7C9E;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin: 8px 0 18px;
}

/* Suggested prompt cards */
.cloud-prompt-card {
    background: #FFFFFF;
    border: 1px solid #E8E2F0;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 12px;
    min-height: 125px;
    box-shadow: 0 3px 12px rgba(91, 67, 138, 0.04);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.cloud-prompt-card:hover {
    border-color: #BBA4DA;
    box-shadow: 0 6px 18px rgba(128, 104, 189, 0.12);
}

.cloud-prompt-icon {
    color: #8068BD;
    font-size: 22px;
    margin-bottom: 8px;
}

.cloud-prompt-card strong {
    display: block;
    color: #49346F;
    font-size: 15px;
    margin-bottom: 6px;
}

.cloud-prompt-card p {
    color: #81748F;
    font-size: 13px;
    margin: 0;
}

@media (max-width: 640px) {
    .cloud-welcome {
        padding: 22px;
    }

    .cloud-welcome h1 {
        font-size: 1.8rem;
    }

    .cloud-prompt-card {
        padding: 14px;
        min-height: 110px;
    }
}


</style>
""", unsafe_allow_html=True)

# -----------------------------------
# Application Branding
# -----------------------------------

st.markdown(
    '<div class="app-title">✦ ContextFlow AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'Your ideas, in better context. '
    'A calmer space to think, learn, and explore.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------------
# 2. Connect to Gemini
# -----------------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("Gemini API key not found. Check secrets.toml.")
    st.stop()

client = genai.Client(api_key=api_key)
# Initialize persistent SQLite storage



# -----------------------------------
# 3. Initialize conversation memory
# -----------------------------------

# -----------------------------------
# Initialize persistent conversation
# -----------------------------------




# -----------------------------------
# Session-Isolated Conversation Initialization
# -----------------------------------

initialize_database()

# Track conversations created in this session
if "owned_chat_ids" not in st.session_state:
    st.session_state.owned_chat_ids = []

# Create a fresh conversation for this session
if "conversation_id" not in st.session_state:
    new_id = create_conversation("New Chat")

    st.session_state.conversation_id = new_id
    st.session_state.owned_chat_ids.append(new_id)

# Load messages for the current conversation
if "messages" not in st.session_state:
    st.session_state.messages = load_messages(
        st.session_state.conversation_id
    )


# -----------------------------------
# Sidebar: Chat Management & Settings
# -----------------------------------

# -----------------------------------
# Conversation management callbacks
# -----------------------------------


def switch_conversation():
    selected_id = st.session_state.conversation_selector

    if selected_id not in st.session_state.owned_chat_ids:
        st.error("This conversation is not available.")
        return

    st.session_state.conversation_id = selected_id
    st.session_state.messages = load_messages(selected_id)


def start_new_conversation():
    new_id = create_conversation("New Chat")

    st.session_state.owned_chat_ids.append(new_id)
    st.session_state.conversation_id = new_id
    st.session_state.messages = []
    st.session_state.conversation_selector = new_id



with st.sidebar:

    
    # -----------------------------------
    # Session-Isolated Conversation Management
    # -----------------------------------
    st.subheader("💬 Your Conversations")

    owned_ids = st.session_state.owned_chat_ids

    # Show only conversations created in this session
    conversations = [
        chat
        for chat in list_conversations()
        if chat[0] in owned_ids
    ]

    chat_titles = {
        chat_id: title
        for chat_id, title, created_at in conversations
    }

    chat_ids = list(chat_titles.keys())
    current_id = st.session_state.conversation_id

    # Synchronize conversation selector
    if (
        "conversation_selector" not in st.session_state
        or st.session_state.conversation_selector not in chat_ids
    ):
        st.session_state.conversation_selector = current_id

   
    st.selectbox(
        "Choose a conversation",
        options=chat_ids,
        format_func=lambda chat_id: chat_titles[chat_id],
        key="conversation_selector",
        on_change=switch_conversation
    )


    st.button(
        "➕ New Chat",
        use_container_width=True,
        on_click=start_new_conversation
    )

    # -----------------------------------
    # Rename Conversation
    # -----------------------------------
    with st.expander("✏️ Rename Chat"):
        new_title = st.text_input(
            "New conversation name",
            value=chat_titles.get(current_id, "New Chat"),
            key=f"rename_input_{current_id}"
        )

        if st.button(
            "Save Name",
            key=f"save_name_{current_id}",
            use_container_width=True
        ):
            if current_id not in owned_ids:
                st.error("Conversation access denied.")

            elif new_title.strip():
                rename_conversation(
                    current_id,
                    new_title.strip()
                )
                st.success("Conversation renamed!")
                st.rerun()

            else:
                st.warning("Please enter a valid name.")

    # -----------------------------------
    # Delete Conversation
    # -----------------------------------
    with st.expander("🗑️ Delete Chat"):
        st.warning(
            "Deleting a conversation permanently removes "
            "its saved messages."
        )

        confirm_delete = st.checkbox(
            "I understand this chat will be deleted.",
            key=f"confirm_delete_{current_id}"
        )

        if st.button(
            "Delete Selected Chat",
            key=f"delete_chat_{current_id}",
            disabled=not confirm_delete,
            use_container_width=True
        ):
            if current_id not in owned_ids:
                st.error("Conversation access denied.")

            else:
                delete_conversation(current_id)

                # Remove the deleted chat from this session
                st.session_state.owned_chat_ids.remove(
                    current_id
                )

                remaining_ids = st.session_state.owned_chat_ids

                if remaining_ids:
                    next_id = remaining_ids[-1]
                else:
                    next_id = create_conversation("New Chat")
                    st.session_state.owned_chat_ids.append(
                        next_id
                    )

                st.session_state.conversation_id = next_id
                st.session_state.messages = load_messages(
                    next_id
                )

                # Reset selector before rerun
                st.session_state.pop(
                    "conversation_selector", None
                )

                st.rerun()

    st.divider()


    # -----------------------------------
    # 2. Chat Settings
    # -----------------------------------
    st.header("⚙️ Chat Settings")




    demo_mode = st.toggle(
        "🧪 Offline Demo Mode",
        value=False,
        help="Use simulated replies without calling Gemini."
    )








    if demo_mode:
        st.info(
            "Demo Mode is active. Replies are simulated "
            "and do not use Gemini."
        )

    max_turns = st.slider(
        "Memory Window (conversation turns)",
        min_value=2,
        max_value=20,
        value=5
    )

    st.caption(
        "Controls how many recent conversation turns "
        "are sent to Gemini."
    )

    st.write(
        f"Messages stored: {len(st.session_state.messages)}"
    )

    st.divider()

    # -----------------------------------
    # 3. Export Conversation
    # -----------------------------------
    st.subheader("📥 Export Conversation")

    if st.session_state.messages:

        chat_text = "\n\n".join(
            f"{message['role'].upper()}:\n"
            f"{message['content']}"
            for message in st.session_state.messages
        )

        st.download_button(
            label="📥 Download Full Chat History",
            data=chat_text,
            file_name=f"contextflow_chat_{current_id}.txt",
            mime="text/plain",
            use_container_width=True,
            on_click="ignore"
        )

    else:
        st.caption("No conversation available to export.")

    st.divider()

    # -----------------------------------
    # Cloud Lilac - Memory Inspector
    # -----------------------------------

    with st.expander("🧠 Memory Inspector", expanded=False):

        total_messages = len(st.session_state.messages)

        user_count = sum(
            1 for msg in st.session_state.messages
            if msg["role"] == "user"
        )

        assistant_count = sum(
            1 for msg in st.session_state.messages
            if msg["role"] == "assistant"
        )

        active_memory = get_recent_history(
            st.session_state.messages,
            max_turns
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Messages", total_messages)
            st.metric("User Messages", user_count)

        with col2:
            st.metric("AI Responses", assistant_count)
            st.metric(
                "Messages in AI Memory",
                len(active_memory)
            )

        if st.checkbox(
            "Show Current AI Memory",
            key="memory_inspector_checkbox"
        ):
            st.json(active_memory)


# -----------------------------------
# Cloud Lilac Studio - Welcome Screen
# -----------------------------------

# Handle clicks on suggested prompts
def choose_suggested_prompt(prompt_text):
    st.session_state.suggested_prompt = prompt_text


# Show welcome screen only for empty conversations
if not st.session_state.messages:




    # -----------------------------------
    # Cloud Lilac - Welcome Panel
    # -----------------------------------
    st.markdown(
        (
            '<div class="cloud-welcome">'
            '<div class="cloud-eyebrow">'
            '✦ YOUR AI WORKSPACE'
            '</div>'
            '<h1>Good to see you.</h1>'
            '<p>'
            'A calmer space to think, learn, and explore. '
            'What would you like to do today?'
            '</p>'
            '</div>'
        ),
        unsafe_allow_html=True
    )







    # Suggestions heading
    st.markdown(
        '<div class="cloud-suggestions">'
        'A LITTLE INSPIRATION TO GET STARTED'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------
    # Interactive Suggestion Cards
    # -----------------------------------
    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.button(
            "⌘  Learn Python",
            key="suggest_python",
            help="Explore Python programming concepts",
            use_container_width=True,
            on_click=choose_suggested_prompt,
            args=("Explain Python programming in simple words.",)
        )

        st.button(
            "✦  Generate Ideas",
            key="suggest_ideas",
            help="Brainstorm creative project ideas",
            use_container_width=True,
            on_click=choose_suggested_prompt,
            args=("Suggest five creative AI project ideas for beginners.",)
        )

    with col2:
        st.button(
            "◈  Explore AI",
            key="suggest_ai",
            help="Learn about artificial intelligence",
            use_container_width=True,
            on_click=choose_suggested_prompt,
            args=("Explain artificial intelligence in simple words.",)
        )

        st.button(
            "◎  Conversation Memory",
            key="suggest_memory",
            help="Understand chatbot memory",
            use_container_width=True,
            on_click=choose_suggested_prompt,
            args=("Explain how conversation memory works in AI chatbots.",)
        )





# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])




# -----------------------------------
# 6. Get user input
# -----------------------------------

# -----------------------------------
# Chat Input + Suggested Prompt Handling
# -----------------------------------

typed_prompt = st.chat_input("Ask ContextFlow AI anything...")

suggested_prompt = st.session_state.pop(
    "suggested_prompt",
    None
)

prompt = suggested_prompt if suggested_prompt else typed_prompt

if prompt is not None:

    if not prompt.strip():
        st.warning("Please enter a valid message.")
        st.stop()

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message in memory
    add_message(
        st.session_state.messages,
        "user",
        prompt.strip()
    )
# User message remains in session memory until
# Gemini successfully responds.
    # Get relevant conversation history
    recent_history = get_recent_history(
        st.session_state.messages,
        max_turns
    )

    # Convert history into Gemini format
    contents = []

    for message in recent_history:
        role = (
            "model"
            if message["role"] == "assistant"
            else "user"
        )

        contents.append(
            types.Content(
                role=role,
                parts=[
                    types.Part.from_text(
                        text=message["content"]
                    )
                ]
            )
        )





    # -----------------------------------
    # Generate AI / Demo Response
    # -----------------------------------
    with st.chat_message("assistant"):
        try:
            start_time = time.perf_counter()

            # -----------------------------------
            # Offline Demo Mode - Simulated Streaming
            # -----------------------------------
            if demo_mode:
                demo_reply = generate_demo_response(
                    prompt.strip()
                )

                def demo_stream():
                    import re

                    for chunk in re.findall(r"\S+\s*", demo_reply):
                        yield chunk
                        time.sleep(0.04)

                reply = st.write_stream(demo_stream())

            # -----------------------------------
            # Gemini AI Mode - Real Streaming
            # -----------------------------------
            else:

                def gemini_stream():
                    for attempt in range(3):
                        received_text = False

                        try:
                            response_stream = (
                                client.models.generate_content_stream(
                                    model="gemini-3.8-flash",
                                    contents=contents,
                                    config=types.GenerateContentConfig(
                                        system_instruction=(
                                            "You are ContextFlow AI, "
                                            "a helpful conversational "
                                            "assistant. Answer clearly "
                                            "and concisely. Use the "
                                            "provided conversation history "
                                            "to maintain context."
                                        ),
                                        max_output_tokens=1024
                                    )
                                )
                            )

                            for chunk in response_stream:
                                if chunk.text:
                                    received_text = True
                                    yield chunk.text

                            return

                        except errors.ServerError as error:
                            # Retry only when no text has been shown
                            if (
                                error.code not in (500, 503, 504)
                                or received_text
                                or attempt == 2
                            ):
                                raise

                            time.sleep(2 ** (attempt + 1))

                reply = st.write_stream(gemini_stream())

            # -----------------------------------
            # Validate Response
            # -----------------------------------
            if not reply or not reply.strip():
                raise ValueError("The model returned no text.")

            # -----------------------------------
            # Calculate Response Time
            # -----------------------------------
            response_time = time.perf_counter() - start_time

            # -----------------------------------
            # Save Exchange to SQLite
            # -----------------------------------
            save_exchange(
                st.session_state.conversation_id,
                prompt.strip(),
                reply
            )

            # -----------------------------------
            # Store Response in Session Memory
            # -----------------------------------
            add_message(
                st.session_state.messages,
                "assistant",
                reply
            )

            # -----------------------------------
            # Display Response Metadata
            # -----------------------------------
            if demo_mode:
                st.caption(
                    "🧪 Simulated response — Demo Mode"
                )

            st.caption(
                f"Response generated in {response_time:.2f} seconds"
            )

        # -----------------------------------
        # Error Handling
        # -----------------------------------
        except Exception as error:
            # Remove unmatched user message from session memory
            if (
                st.session_state.messages
                and st.session_state.messages[-1]["role"] == "user"
            ):
                st.session_state.messages.pop()

            error_code = getattr(error, "code", None)

            if error_code == 429:
                st.error(
                    "Gemini API quota exceeded. "
                    "Please try again after your quota resets."
                )

            elif error_code in (500, 503, 504):
                st.error(
                    "Gemini is temporarily unavailable. "
                    "Please try again later."
                )

            else:
                st.error(
                    "Unable to generate a response. "
                    "Please check your configuration."
                )

            st.caption(
                f"Technical details: {error}"
            )




# -----------------------------------
# Developer Portfolio Footer
# -----------------------------------


st.markdown("""
<style>

/* Cloud Lilac Studio - Developer Footer */

.developer-footer {
    margin-top: 36px;
    padding: 22px 26px;
    border: 1px solid #E8E2F0;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        #FFFFFF,
        #F5F0FB
    );
    box-shadow: 0 6px 24px rgba(91, 67, 138, 0.05);
}

.developer-footer-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}

.developer-label {
    color: #8B7C9E;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.4px;
}

.developer-name {
    color: #5B438A;
    font-size: 21px;
    font-weight: 700;
    margin-top: 5px;
}

.developer-tagline {
    color: #81748F;
    font-size: 12px;
    margin-top: 5px;
}

.developer-github {
    display: inline-block;
    background: #8068BD;
    color: #FFFFFF !important;
    padding: 10px 18px;
    border: 1px solid #8068BD;
    border-radius: 24px;
    font-size: 12px;
    font-weight: 600;
    text-decoration: none !important;
    transition: all 0.2s ease;
}

.developer-github:hover {
    background: #6A52A6;
    border-color: #6A52A6;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(128, 104, 189, 0.18);
    transform: translateY(-2px);
}

.developer-footer-bottom {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
    border-top: 1px solid #E8E2F0;
    margin-top: 18px;
    padding-top: 12px;
    color: #988BA7;
    font-size: 11px;
}

</style>
""", unsafe_allow_html=True)

# HTML kept as a single Python string to prevent
# multiline HTML rendering and syntax issues.

footer_html = (
    '<div class="developer-footer">'
    '<div class="developer-footer-top">'
    '<div>'
    '<div class="developer-label">DESIGNED &amp; DEVELOPED BY</div>'
    '<div class="developer-name">Humeesa</div>'
    '<div class="developer-tagline">'
    'Turning ideas into intelligent experiences.'
    '</div>'
    '</div>'
    '<a class="developer-github" '
    'href="https://github.com/humeesao126-pixel" '
    'target="_blank" rel="noopener noreferrer">'
    'Explore GitHub ↗'
    '</a>'
    '</div>'
    '<div class="developer-footer-bottom">'
    '<span>© 2026 · All rights reserved</span>'
    '<span>Built with Python · Streamlit · Gemini</span>'
    '</div>'
    '</div>'
)

st.markdown(footer_html, unsafe_allow_html=True)
