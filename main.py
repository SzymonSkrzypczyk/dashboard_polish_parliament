import streamlit as st
import matplotlib.pyplot as plt
from fetch_data import get_clubs, get_members_by_club, get_all_by_term, get_all_proceedings, get_all_interpellations

st.set_page_config(layout="wide")
st.title("Dashboard Sejmu RP")

clubs = get_clubs()
club_names = [(club['name'], club["id"]) for club in clubs]

selected_clubs = st.sidebar.multiselect("Wybierz partie", [name for name, _ in club_names])

selected_term = st.sidebar.slider("Wybierz kadencje", 1, 10, 10)

# for selected_club in selected_clubs:
#     club_id = next((club['id'] for club in clubs if club['name'] == selected_club), None)
col1, col2, col3 = st.columns(3, gap="large", vertical_alignment="center")

all_mps = get_all_by_term(selected_term)
all_active = [mp for mp in all_mps if mp["active"] is True]
mps_by_party = {party_id: len(get_members_by_club(party_id, selected_term)) for _, party_id in club_names}

mps_by_education = {
    education: len([mp for mp in all_mps if mp.get("educationLevel") is not None and mp["educationLevel"] == education])
    for education in set([edu["educationLevel"] for edu in all_mps if edu.get("educationLevel") is not None])
}
mps_by_voivo = {
    voivodeship: len([mp for mp in all_mps if mp.get("voivodeship") is not None and mp["voivodeship"] == voivodeship])
    for voivodeship in set([voivo["voivodeship"] for voivo in all_mps if voivo.get("voivodeship") is not None])
}
mps_by_prof = {
    profession: len([mp for mp in all_mps if mp.get("profession") is not None and mp["profession"] == profession])
    for profession in set([voivo["profession"] for voivo in all_mps if voivo.get("profession") is not None])
}

all_proceedings = len(get_all_proceedings(selected_term))
all_interpellations = len(get_all_interpellations(selected_term))
print(mps_by_prof)

with col1:
    # liczba aktywnych poslow V
    # rozklad procentowy poslow na kluby V
    st.markdown(f"""
        <div style='text-align: center; border: solid black 1px; border-radius: 10px;'>
            <p style='font-size:14px; color:gray; margin-bottom: 0;'>Wszystkich Posłów</p>
            <p style='font-size:36px; font-weight:bold; margin-top: 0;'>{len(all_mps)}</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # wyksztalcenie poslow V
    # wojewodztwa z ktorych sa V
    # po zawodzie
    st.text("2")

with col3:
    # liczba posiedzen V
    # liczba interapelacji V
    st.text("3")
