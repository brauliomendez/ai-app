import streamlit as st

from translator import translate

if "language" not in st.session_state:
    st.session_state.language = "es"

st.set_page_config(page_icon="🅱️")

with st.sidebar:
    toggle_label = (
        translate("app.sidebar.switch_to_spanish")
        if st.session_state.language == "en"
        else translate("app.sidebar.switch_to_english")
    )
    if st.button(toggle_label):
        st.session_state.language = "es" if st.session_state.language == "en" else "en"
        st.rerun()

    api_key_value = st.text_input(
        translate("app.sidebar.api_key_label"),
        value=st.session_state.get("openai_api_key", ""),
        type="default",
    )
    if api_key_value:
        st.session_state.openai_api_key = api_key_value

home = st.Page("home.py", title=translate("navigation.home"))
chat = st.Page("chat.py", title=translate("navigation.chat"))
rag = st.Page("rag.py", title=translate("navigation.rag"))
images = st.Page("images.py", title=translate("navigation.images"))
audio = st.Page("audio.py", title=translate("navigation.audio"))
testing = st.Page("testing.py", title=translate("navigation.testing"))
about = st.Page("about.py", title=translate("navigation.about"))

pg = st.navigation([home, chat, rag, images, audio, testing, about])
pg.run()
