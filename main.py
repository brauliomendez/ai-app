import hashlib

import streamlit as st

from translator import translate

PASSWORD_HASH = "5be25fc74181503836a6056b06e251487edfc43dca1ccae2603dd308c9c2239d"


def verify_password(raw_password: str) -> bool:
    candidate_hash = hashlib.sha256(raw_password.encode()).hexdigest()
    return candidate_hash == PASSWORD_HASH


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "language" not in st.session_state:
    st.session_state.language = "es"

if not st.session_state.authenticated:
    with st.form("login_form"):
        password = st.text_input(
            translate("app.login.password_label"),
            type="default",
        )
        submitted = st.form_submit_button(translate("app.login.submit_button"))
        if submitted:
            if verify_password(password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(translate("app.login.error_message"))
    st.stop()

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

home = st.Page("home.py", title=translate("navigation.home"))
chat = st.Page("chat.py", title=translate("navigation.chat"))
rag = st.Page("rag.py", title=translate("navigation.rag"))
images = st.Page("images.py", title=translate("navigation.images"))
audio = st.Page("audio.py", title=translate("navigation.audio"))
testing = st.Page("testing.py", title=translate("navigation.testing"))
about = st.Page("about.py", title=translate("navigation.about"))

pg = st.navigation([home, chat, rag, images, audio, testing, about])
pg.run()
