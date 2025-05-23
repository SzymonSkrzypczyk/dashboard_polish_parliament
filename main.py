import streamlit as st
import plotly.express as px
from fetch_data import get_clubs, get_members_by_club, get_all_by_term, get_all_proceedings, get_all_interpellations

st.set_page_config(layout="wide")
st.title("Dashboard Sejmu RP")

clubs = get_clubs()
club_names = [(club['name'], club["id"]) for club in clubs]

selected_clubs = st.sidebar.multiselect("Wybierz partie", [name for name, _ in club_names])
selected_term = st.sidebar.slider("Wybierz kadencje", 1, 10, 10)

col1, col2, col3 = st.columns(3, gap="large", vertical_alignment="center")

all_mps = get_all_by_term(selected_term)
all_active = [mp for mp in all_mps if mp["active"] is True]
mps_by_party = {party_id: len(get_members_by_club(party_id, selected_term)) for _, party_id in club_names}

mps_by_education = {
    education: len([mp for mp in all_mps if mp.get("educationLevel") == education])
    for education in set(mp["educationLevel"] for mp in all_mps if mp.get("educationLevel"))
}
mps_by_voivo = {
    voivodeship: len([mp for mp in all_mps if mp.get("voivodeship") == voivodeship])
    for voivodeship in set(mp["voivodeship"] for mp in all_mps if mp.get("voivodeship"))
}
mps_by_prof = {
    profession: len([mp for mp in all_mps if mp.get("profession") == profession])
    for profession in set(mp["profession"] for mp in all_mps if mp.get("profession"))
}

all_proceedings = len(get_all_proceedings(selected_term))
all_interpellations = len(get_all_interpellations(selected_term))

with col1:
    st.markdown("### Posłowie według klubów")
    clubs_sorted = sorted(mps_by_party.items(), key=lambda x: x[1], reverse=True)
    club_labels = [next((name for name, cid in club_names if cid == club_id), club_id) for club_id, _ in clubs_sorted]
    fig = px.bar(
        x=[count for _, count in clubs_sorted],
        y=club_labels,
        orientation='h',
        labels={'x': 'Liczba posłów', 'y': 'Klub'},
        title='Posłowie według klubów',
        color_discrete_sequence=['mediumpurple']
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Procentowy udział wykształcenia")
    fig = px.pie(
        names=list(mps_by_education.keys()),
        values=list(mps_by_education.values()),
        title="Wykształcenie",
        hole=0,
    )
    fig.update_traces(
        textinfo='none',
        hovertemplate='%{label}: %{percent} (%{value})'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Liczba aktywnych posłów")
    st.markdown(f"""
        <div style='text-align: center; border: solid black 1px; border-radius: 10px; padding: 10px;'>
            <p style='font-size:14px; color:gray; margin-bottom: 0;'>Aktywni posłowie</p>
            <p style='font-size:36px; font-weight:bold; margin-top: 0;'>{len(all_active)}</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### Wykształcenie Posłów")
    fig = px.bar(
        x=list(mps_by_education.values()),
        y=list(mps_by_education.keys()),
        orientation='h',
        labels={'x': 'Liczba posłów', 'y': 'Wykształcenie'},
        title='Wykształcenie Posłów',
        color_discrete_sequence=['skyblue']
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Województwa posłów")
    fig = px.bar(
        x=list(mps_by_voivo.values()),
        y=list(mps_by_voivo.keys()),
        orientation='h',
        labels={'x': 'Liczba posłów', 'y': 'Województwo'},
        title='Województwa posłów',
        color_discrete_sequence=['lightgreen']
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Zawody posłów")
    prof_items = sorted(mps_by_prof.items(), key=lambda x: x[1], reverse=True)[:10]
    fig = px.bar(
        x=[item[1] for item in prof_items],
        y=[item[0] for item in prof_items],
        orientation='h',
        labels={'x': 'Liczba posłów', 'y': 'Zawód'},
        title='Top 10 zawodów posłów',
        color_discrete_sequence=['salmon']
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

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
    top_voivos = sorted(mps_by_voivo.items(), key=lambda x: x[1], reverse=True)[:10]
    labels = [name for name, _ in top_voivos]
    counts = [count for _, count in top_voivos]
    fig = px.pie(
        names=labels,
        values=counts,
        title="Top 10 województw wg liczby posłów",
        hole=0,
    )
    fig.update_traces(
        textinfo='none',
        hovertemplate='%{label}: %{percent} (%{value})'
    )
    st.plotly_chart(fig, use_container_width=True)
