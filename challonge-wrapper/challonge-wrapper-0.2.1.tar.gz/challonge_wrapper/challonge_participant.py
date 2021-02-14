from .challonge_helpers import fetch_raw_data, TOURNAMENT_URL

class ChallongeParticipant:
    def __init__(self, players_json):
        # id is tournament-specific
        self._id = players_json['id']
        self._name = players_json['challonge_username'] or players_json['name']
        self._seed = players_json['seed']
        self._position = players_json['final_rank']
        self._signup_date = players_json['created_at'].split("T")[0]
        self._signup_time = players_json['created_at'].split("T")[1]

    def __str__(self):
        return "[id: {}, seed: {}, name: {}]".format(
            self.id, self.seed, self.name
        )

    def __repr__(self):
        return str(self)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def seed(self):
        return self._seed

    @property
    def position(self):
        return self._position

    @property
    def signup_date(self):
        return self._signup_date

    @property
    def signup_time(self):
        return self._signup_time

# will initialize and contain a list of ChallongeParticipants elements
def init_participants(url, community=''):
    # formats URLs accordingly
    if community != None:
        api_url = f"{TOURNAMENT_URL}{community}{'-'}{url}{'/participants.json'}"
    else:
        api_url = f"{TOURNAMENT_URL}{url}{'/participants.json'}"

    raw_players = fetch_raw_data(api_url)

    players = []
    for i in range(0, len(raw_players)):
        players.append(ChallongeParticipant(
            raw_players[i]['participant'])
        )

    return players
