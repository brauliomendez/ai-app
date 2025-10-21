import streamlit as st

from translator import translate

st.title(translate("about.title"))

st.write(translate("about.body"))
