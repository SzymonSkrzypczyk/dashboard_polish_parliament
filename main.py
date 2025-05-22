import streamlit as st

st.title("dupa")

with st.sidebar:
    st.header("Settings")

    party = st.selectbox("Party", ["P1", "P2", "P3", "P4", "P5"])
