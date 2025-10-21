import streamlit as st
from openai import OpenAI

import env_secrets
from translator import translate

OPENAI_API_KEY = env_secrets.OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def stream_gpt_response(chat_history, placeholder):
    """Stream the assistant response while keeping markdown formatting."""
    text_chunks = []
    try:
        with client.responses.stream(
            model="gpt-5-mini",
            input=chat_history,
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    text_chunks.append(event.delta)
                    placeholder.markdown("".join(text_chunks))
                elif event.type == "response.completed":
                    return event.response.output_text
    except Exception as exc:
        placeholder.error(translate("chat.error_message", error=str(exc)))
        return None

    return "".join(text_chunks)


def reset_chat_history():
    st.session_state.chat_history = [
        {"role": "assistant", "content": translate("chat.default_assistant_message")}
    ]


if "chat_history" not in st.session_state:
    reset_chat_history()

col1, col2 = st.columns(2)
with col1:
    st.header(translate("chat.header"))
with col2:
    if st.button(translate("chat.clear_history"), type="secondary"):
        reset_chat_history()

for message in st.session_state.chat_history:
    st.chat_message(message["role"]).markdown(message["content"])

if prompt := st.chat_input(translate("chat.input_placeholder")):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    assistant_message = st.chat_message("assistant")
    message_placeholder = assistant_message.empty()

    response = stream_gpt_response(st.session_state.chat_history, message_placeholder)

    if response:
        st.session_state.chat_history.append({"role": "assistant", "content": response})
