import streamlit as st

from translator import translate

st.title(translate("home.title"))

st.header(translate("home.index_header"), divider="rainbow")

st.page_link("chat.py", label=translate("home.link.chat"))
st.page_link("rag.py", label=translate("home.link.rag"))
st.page_link("images.py", label=translate("home.link.images"))
st.page_link("audio.py", label=translate("home.link.audio"))
