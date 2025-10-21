import streamlit as st
import pandas as pd
import numpy as np

from translator import translate

st.title(translate("testing.title"))

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.caption(translate("testing.caption", count=st.session_state.counter))

st.header(translate("testing.interactions_header"), divider=True)

col1, col2 = st.columns(2)

with col1:
    x = st.slider(translate("testing.slider_label"), 1, 100)
with col2:
    st.write(translate("testing.slider_value", value=x))

st.header(translate("testing.editable_header"), divider=True)

df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
)
edited_df = st.data_editor(df, num_rows="dynamic")

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(translate("testing.favorite_command", command=favorite_command))

st.header(translate("testing.cool_chart_header"), divider="blue")
st.badge(translate("testing.success_badge"), icon=":material/check:", color="green")

chart_data = pd.DataFrame(np.random.randn(20, 4), columns=["a", "b", "c", "d"])
st.area_chart(chart_data)

st.header(translate("testing.map_header"), divider="green")

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [20, 20] + [43.370971, -8.402824],
    columns=["lat", "lon"],
)

if st.checkbox(translate("testing.map_checkbox")):
    st.map(map_data, color="#85492e")
