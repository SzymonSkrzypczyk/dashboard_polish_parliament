import streamlit as st
import plotly.express as px
from fetch_data import get_clubs, get_members_by_club, get_by_term, get_timeframe

st.set_page_config(layout="wide")
st.title("Dashboard Sejmu RP")

selected_term = st.sidebar.slider("Wybierz kadencje", 1, 10, 10)
term_dates = get_timeframe(selected_term)

# Display term dates
st.sidebar.markdown("### Daty kadencji")
st.sidebar.markdown(f"""
    <div style='text-align: center; border: solid black 1px; border-radius: 10px; padding: 10px;'>
        <p style='font-size:14px; color:gray; margin-bottom: 0;'>Od</p>
        <p style='font-size:36px; font-weight:bold; margin-top: 0;'>{term_dates['from']}</p>
        <p style='font-size:14px; color:gray; margin-bottom: 0;'>Do</p>
        <p style='font-size:36px; font-weight:bold; margin-top: 0;'>{term_dates['to'] if term_dates['to'] else ''}</p>
    </div>
""", unsafe_allow_html=True)

if selected_term < 4:
    st.sidebar.warning("Dla mniejszych kadencji API sejmu nie zwraca dobrych wartości(z reguły)")

clubs = get_clubs(selected_term)
club_names = [(club['name'], club["id"]) for club in clubs]
club_id2name = {club["name"]: club["id"] for club in clubs}

all_mps = get_by_term(selected_term, "MP")
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

all_proceedings = len(get_by_term(selected_term, "proceedings"))
all_interpellations = len(get_by_term(selected_term, "interpellations"))

# --- First row ---
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

with row1_col1:
    st.markdown("### Liczba interpelacji")
    st.markdown(f"""
            <div style='text-align: center; border: solid black 1px; border-radius: 10px; padding: 10px;'>
                <p style='font-size:14px; color:gray; margin-bottom: 0;'>Liczba interpelacji</p>
                <p style='font-size:36px; font-weight:bold; margin-top: 0;'>{all_interpellations if all_interpellations > 0 else "N/A"}</p>
            </div>
        """, unsafe_allow_html=True)

with row1_col2:
    st.markdown("### Liczba posiedzeń")
    st.markdown(f"""
            <div style='text-align: center; border: solid black 1px; border-radius: 10px; padding: 10px;'>
                <p style='font-size:14px; color:gray; margin-bottom: 0;'>Liczba posiedzeń</p>
                <p style='font-size:36px; font-weight:bold; margin-top: 0;'>{all_proceedings if all_proceedings > 0 else "N/A"}</p>
            </div>
        """, unsafe_allow_html=True)

with row1_col3:
    st.markdown("### Liczba aktywnych posłów")
    st.markdown(f"""
        <div style='text-align: center; border: solid black 1px; border-radius: 10px; padding: 10px;'>
            <p style='font-size:14px; color:gray; margin-bottom: 0;'>Aktywni posłowie</p>
            <p style='font-size:36px; font-weight:bold; margin-top: 0;'>{number_active if (number_active := len(all_active)) > 0 else "N/A"}</p>
        </div>
    """, unsafe_allow_html=True)

with row1_col4:
    st.markdown("### Liczba wszystkich posłów")
    st.markdown(f"""
        <div style='text-align: center; border: solid black 1px; border-radius: 10px; padding: 10px;'>
            <p style='font-size:14px; color:gray; margin-bottom: 0;'>Wszyscy posłowie</p>
            <p style='font-size:36px; font-weight:bold; margin-top: 0;'>{number_mps if (number_mps := len(all_mps)) > 0 else "N/A"}</p>
        </div>
    """, unsafe_allow_html=True)

# --- Second row ---
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.markdown("### Wykształcenie Posłów")
    if mps_by_education:
        sorted_edu = sorted(mps_by_education.items(), key=lambda x: x[1], reverse=True)
        fig = px.bar(
            x=[count for _, count in sorted_edu],
            y=[edu for edu, _ in sorted_edu],
            orientation='h',
            labels={'x': 'Liczba posłów', 'y': 'Wykształcenie'},
            title='Wykształcenie Posłów',
            color_discrete_sequence=['skyblue']
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("Nie znaleziono danych o wykształceniu posłów.")

with row2_col2:
    st.markdown("### Województwa posłów")
    if mps_by_voivo:
        sorted_voivos = sorted(mps_by_voivo.items(), key=lambda x: x[1], reverse=True)

        fig = px.bar(
            x=[count for _, count in sorted_voivos],
            y=[voivo for voivo, _ in sorted_voivos],
            orientation='h',
            labels={'x': 'Liczba posłów', 'y': 'Województwo'},
            title='Województwa posłów',
            color_discrete_sequence=['lightgreen']
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("Nie znaleziono danych o województwach posłów.")

with row2_col3:
    st.markdown("### Zawody posłów")
    prof_items = sorted(mps_by_prof.items(), key=lambda x: x[1], reverse=True)[:10]
    if prof_items:
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
    else:
        st.markdown("Nie znaleziono danych o zawodach posłów.")

# --- Third row ---
row3_col1, row3_col2, row3_col3 = st.columns(3)

with row3_col1:
    st.markdown("### Procentowy udział wykształcenia")
    if mps_by_education:
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
    else:
        st.markdown("Nie znaleziono danych o wykształceniu posłów.")

with row3_col2:
    st.markdown("### Posłowie według partii")
    clubs_sorted = sorted(mps_by_party.items(), key=lambda x: x[1], reverse=True)
    if clubs_sorted:
        club_labels = [next((cid for name, cid in club_names if cid == club_id), club_id) for club_id, _ in clubs_sorted]
        hover_texts = [f"{club_id2name.get(club_id, club_id)}: {count} posłów" for club_id, count in clubs_sorted]
        fig = px.bar(
            x=[count for _, count in clubs_sorted],
            y=club_labels,
            orientation='h',
            labels={'x': 'Liczba posłów', 'y': 'Partia'},
            title='Posłowie według partii',
            color_discrete_sequence=['mediumpurple']
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("Nie znaleziono danych o partiach posłów.")

with row3_col3:
    st.markdown("### Procentowy udział województw")
    if mps_by_voivo:
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
    else:
        st.markdown("Nie znaleziono danych o województwach posłów.")