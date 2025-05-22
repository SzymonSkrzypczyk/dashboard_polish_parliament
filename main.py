import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch_data import get_clubs, get_members_by_club

st.title("Dashboard Sejmu RP")

clubs = get_clubs()
club_names = [club['name'] for club in clubs]

selected_clubs = st.sidebar.multiselect("Wybierz partie", club_names)

selected_term = st.sidebar.slider("Wybierz kadencje", 1, 10, 10)

if selected_clubs:
    # for selected_club in selected_clubs:
    #     club_id = next((club['id'] for club in clubs if club['name'] == selected_club), None)
    col1, col2, col3 = st.columns(3, gap="medium", vertical_alignment="center")

    with col1:
        # liczba aktywnych poslow
        # rozklad procentowy poslow na kluby
        st.text("1")

    with col2:
        # wyksztalcenie poslow
        # wojewodztwa z ktorych sa
        st.text("2")

    with col3:
        # liczba posiedzen
        # liczba interapelacji
        st.text("3")


else:
    st.info("Proszę wybrać co najmniej jedną partię z paska bocznego.")
