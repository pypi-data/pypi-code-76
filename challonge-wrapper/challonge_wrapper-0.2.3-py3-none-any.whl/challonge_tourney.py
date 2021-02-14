import os
import json

from .challonge_participant import init_participants
from .challonge_match import init_matches
from .challonge_helpers import fetch_raw_data

TOURNEY_URL = "https://api.challonge.com/v1/tournaments/"

class ChallongeTourney:
    def __init__(self, raw_data):    
        self._id = raw_data['id']
        self._name = raw_data['name']
        self._community = raw_data['subdomain']
        self._tournament_type = raw_data['tournament_type']
        self._description = raw_data['description']
        self._players_num = raw_data['participants_count']
        self._game_name = raw_data['game_name']
        self._start_date = raw_data['started_at'].split("T")[0]
        self._start_time = raw_data['started_at'].split("T")[1]
        self._create_date = raw_data['created_at'].split("T")[0]
        self._create_time = raw_data['created_at'].split("T")[1]
        self._url = raw_data['url']

        self._matches = []
        self._players = []
        
    def __str__(self):
        return 'id: {}, name: {}, players: {}, game: {}, start: {}'.format(
            self._id, self._name, self._players_num, 
            self._game_name, self._start_date, self._start_time
        )

    def __eq__(self, other):
        if isinstance(other, ChallongeTourney) and self._id == other.id:
            return True
        return False

    def __repr__(self):
        return str(self)

    # ChallongeTourney properties
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def tournament_type(self):
        return self._tournament_type

    @property
    def description(self):
        return self._description

    @property
    def game_name(self):
        return self._game_name

    @property
    def start_date(self):
        return self._start_time

    @property
    def start_time(self):
        return self._start_time

    @property
    def create_date(self):
        return self._create_date

    @property
    def create_time(self):
        return self._create_time

    @property
    def url(self):
        return self._url

    @property
    def community(self):
        return self._community

    @property
    def participants(self):
        return self._players

    @property
    def matches(self):
        return self._matches

def init_tourney(slug, community='', participants=False, matches=False):
    # formats URLs accordingly
    if community != '':
        api_url = TOURNEY_URL + community + '-' + slug + ".json"
    else:
        api_url = TOURNEY_URL + slug + ".json"

    # gets raw data from challonge as a json file
    raw_data = fetch_raw_data(api_url)['tournament']

    # checks whether the tournament has started
    if raw_data['state'] in ("pending", "ongoing", "checking_in", "underway"):
        print("bracket hasn't started yet or it's underway.")
        raise SystemExit()

    # creates ChallongeTourney object
    newTournament = ChallongeTourney(raw_data)

    if participants == True:
        newTournament._players = init_participants(slug, community)

    if matches == True:
        newTournament._matches = init_matches(slug, community, newTournament._players)

    return newTournament
