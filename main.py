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

with col1:
    st.markdown("### Posłowie według klubów")
    fig, ax = plt.subplots()
    clubs_sorted = sorted(mps_by_party.items(), key=lambda x: x[1], reverse=True)
    club_labels = [next((name for name, cid in club_names if cid == club_id), club_id) for club_id, _ in clubs_sorted]
    ax.barh(club_labels, [count for _, count in clubs_sorted], color='mediumpurple')
    ax.set_xlabel("Liczba posłów")
    ax.invert_yaxis()
    st.pyplot(fig)

    st.markdown("### Procentowy udział wykształcenia")
    fig, ax = plt.subplots()
    ax.pie(mps_by_education.values(), labels=mps_by_education.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.markdown("### Liczba aktywnych posłów")
    st.markdown(f"""
        <div style='text-align: center; border: solid black 1px; border-radius: 10px; padding: 10px;'>
            <p style='font-size:14px; color:gray; margin-bottom: 0;'>Aktywni posłowie</p>
            <p style='font-size:36px; font-weight:bold; margin-top: 0;'>{len(all_active)}</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### Wykształcenie Posłów")
    fig, ax = plt.subplots()
    ax.barh(list(mps_by_education.keys()), list(mps_by_education.values()), color='skyblue')
    ax.set_xlabel("Liczba posłów")
    st.pyplot(fig)

    st.markdown("### Województwa posłów")
    fig, ax = plt.subplots()
    ax.barh(list(mps_by_voivo.keys()), list(mps_by_voivo.values()), color='lightgreen')
    ax.set_xlabel("Liczba posłów")
    st.pyplot(fig)

    st.markdown("### Zawody posłów")
    fig, ax = plt.subplots()
    prof_items = sorted(mps_by_prof.items(), key=lambda x: x[1], reverse=True)[:10]  # top 10
    ax.barh([item[0] for item in prof_items], [item[1] for item in prof_items], color='salmon')
    ax.set_xlabel("Liczba posłów")
    ax.set_title("Top 10 zawodów posłów")
    st.pyplot(fig)

with col3:
    with col3:
        st.markdown("### Statystyki prac Sejmu")

        st.markdown(f"""
            <div style='text-align: center; border: solid black 1px; border-radius: 10px; padding: 10px;'>
                <p style='font-size:14px; color:gray; margin-bottom: 0;'>Liczba posiedzeń</p>
                <p style='font-size:36px; font-weight:bold; margin-top: 0;'>{all_proceedings}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style='text-align: center; border: solid black 1px; border-radius: 10px; padding: 10px; margin-top: 20px;'>
                <p style='font-size:14px; color:gray; margin-bottom: 0;'>Liczba interpelacji</p>
                <p style='font-size:36px; font-weight:bold; margin-top: 0;'>{all_interpellations}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### Procentowy udział województw")
        fig, ax = plt.subplots()
        top_voivos = sorted(mps_by_voivo.items(), key=lambda x: x[1], reverse=True)[:10]
        ax.pie([count for _, count in top_voivos], labels=[name for name, _ in top_voivos], autopct='%1.1f%%',
               startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
