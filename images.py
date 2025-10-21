import base64
from io import BytesIO

import streamlit as st
from openai import OpenAI

from translator import translate


def get_client() -> OpenAI:
    api_key = st.session_state.get("openai_api_key")
    if not api_key:
        raise ValueError(translate("images.missing_api_key"))
    return OpenAI(api_key=api_key)

SIZE_OPTIONS = [
    ("images.size_option.rectangle", "1024x1024"),
    ("images.size_option.landscape", "1536x1024"),
    ("images.size_option.portrait", "1024x1536"),
]
SIZE_LOOKUP = {key: value for key, value in SIZE_OPTIONS}
SIZE_KEYS = [key for key, _ in SIZE_OPTIONS]

if "image_prompt" not in st.session_state:
    st.session_state.image_prompt = None

if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None

if "image_size_key" not in st.session_state:
    st.session_state.image_size_key = SIZE_KEYS[0]


def generate_image(prompt: str, size: str) -> bytes:
    """Generate an image using OpenAI and return its bytes."""
    client = get_client()
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size=size,
        quality="high",
        n=1,
    )
    image_base64 = response.data[0].b64_json
    return base64.b64decode(image_base64)


st.title(translate("images.title"))
st.caption(translate("images.caption"))

st.session_state.image_size_key = st.selectbox(
    translate("images.size_label"),
    options=SIZE_KEYS,
    index=SIZE_KEYS.index(st.session_state.image_size_key),
    format_func=lambda option_key: translate(option_key),
)

if prompt := st.chat_input(translate("images.prompt_placeholder")):
    st.session_state.image_prompt = prompt
    with st.spinner(translate("images.spinner")):
        try:
            st.session_state.image_bytes = generate_image(
                prompt, SIZE_LOOKUP[st.session_state.image_size_key]
            )
        except Exception as exc:
            st.session_state.image_bytes = None
            st.error(translate("images.error_message", error=str(exc)))

if st.session_state.image_bytes:
    st.subheader(translate("images.generated_header"))
    st.image(
        st.session_state.image_bytes,
        caption=st.session_state.image_prompt,
        width="stretch",
    )

    download_buffer = BytesIO(st.session_state.image_bytes)
    download_buffer.seek(0)
    st.download_button(
        translate("images.download_button"),
        data=download_buffer,
        file_name="generated-image.png",
        mime="image/png",
    )
