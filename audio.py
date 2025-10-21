from io import BytesIO

import streamlit as st
from openai import OpenAI

from translator import translate
import util


def get_client() -> OpenAI:
    api_key = st.session_state.get("openai_api_key")
    if api_key and len(api_key) < 30:
        api_key = util.decrypt(api_key)
    if not api_key:
        raise ValueError(translate("audio.missing_api_key"))
    return OpenAI(api_key=api_key)

VOICE_OPTIONS = [
    "alloy",
    "ash",
    "ballad",
    "coral",
    "echo",
    "fable",
    "onyx",
    "nova",
    "sage",
    "shimmer",
    "verse",
]

if "tts_text" not in st.session_state:
    st.session_state.tts_text = ""

if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = None

if "tts_voice" not in st.session_state:
    st.session_state.tts_voice = VOICE_OPTIONS[0]


def synthesize_speech(text: str, voice: str) -> bytes:
    client = get_client()
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
    )
    return response.read()


st.title(translate("audio.title"))
st.caption(translate("audio.caption"))

col_input, col_button = st.columns([3, 1])

with col_input:
    st.session_state.tts_text = st.text_area(
        translate("audio.text_area_label"),
        value=st.session_state.tts_text,
        height=150,
    )

with col_button:
    generate_clicked = st.button(
        translate("audio.generate_button"), use_container_width=True
    )
    st.session_state.tts_voice = st.selectbox(
        translate("audio.voice_label"),
        options=VOICE_OPTIONS,
        index=VOICE_OPTIONS.index(st.session_state.tts_voice),
    )

if generate_clicked and st.session_state.tts_text.strip():
    with st.spinner(translate("audio.spinner")):
        try:
            st.session_state.tts_audio = synthesize_speech(
                st.session_state.tts_text, st.session_state.tts_voice
            )
        except Exception as exc:
            st.session_state.tts_audio = None
            st.error(translate("audio.error_message", error=str(exc)))

if st.session_state.tts_audio:
    st.subheader(translate("audio.generated_header"))
    st.audio(st.session_state.tts_audio, format="audio/mp3")

    download_buffer = BytesIO(st.session_state.tts_audio)
    download_buffer.seek(0)
    st.download_button(
        translate("audio.download_button"),
        data=download_buffer,
        file_name="speech.mp3",
        mime="audio/mpeg",
    )
