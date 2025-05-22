from dataclasses import dataclass
from string import Template
import requests

BASE_URL = Template("https://api.sejm.gov.pl/sejm/term$term")


@dataclass
class MP:
    first_name: str
    last_name: str
    club: str
    active: bool
    educationLevel: str
    profession: str
    voivodeship: str
    numberOfVotes: int


def get_clubs(term: int = 10):
    response = requests.get(f"{BASE_URL.substitute(term=term)}/clubs")
    if response.status_code == 200:
        return response.json()
    else:
        return []


def get_all_by_term(term: int = 10):
    response = requests.get(f"{BASE_URL.substitute(term=term)}/MP")
    if response.status_code == 200:
        members = response.json()
        # educationLevel, active, profession, voivodeship
        return members
    else:
        return []


def get_all_interpellations(term: int = 10):
    response = requests.get(f"{BASE_URL.substitute(term=term)}/interpellations")
    if response.status_code == 200:
        interpellations = response.json()
        return interpellations
    else:
        return []


def get_all_prints(term: int = 10):
    response = requests.get(f"{BASE_URL.substitute(term=term)}/prints")
    if response.status_code == 200:
        prints = response.json()
        return prints
    else:
        return []


def get_all_proceedings(term: int = 10):
    response = requests.get(f"{BASE_URL.substitute(term=term)}/proceedings")
    if response.status_code == 200:
        proceedings = response.json()
        return proceedings
    else:
        return []


def get_votings_per_day(term: int = 10):
    response = requests.get(f"{BASE_URL.substitute(term=term)}/proceedings")
    if response.status_code == 200:
        proceedings = response.json()
        return proceedings
    else:
        return []


def get_members_by_club(club_id: str, term: int = 10):
    response = requests.get(f"{BASE_URL.substitute(term=term)}/MP")
    if response.status_code == 200:
        members = response.json()
        # educationLevel, active, profession, voivodeship
        return [member for member in members if member.get('club') == club_id]
    else:
        return []


if __name__ == '__main__':
    print(get_members_by_club("KO"))
