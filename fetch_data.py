from dataclasses import dataclass
from typing import Literal
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


def get_timeframe(term: int = 10):
    response = requests.get(f"{BASE_URL.substitute(term=term)}")
    from_date = None
    to_date = None
    if response.status_code == 200:
        timeframe = response.json()
        from_date = timeframe["from"]
        to_date = timeframe.get("to", None)

    return {"from": from_date, "to": to_date}


def get_by_term(term: int = 10, target: Literal["MP", "interpellations", "prints", "proceedings"] = "MP"):
    response = requests.get(f"{BASE_URL.substitute(term=term)}/{target}")
    if response.status_code == 200:
        data = response.json()
        return data
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
