from .challonge_helpers import (TOURNAMENT_URL, get_player_name, 
                            assign_round_names, fetch_raw_data)

class ChallongeMatch:
    def __init__(self, matches_json, nicknames, round_names):
        # ids are tournament-specific
        self._id = matches_json['id']
        self._score = matches_json['scores_csv']
        self._p1_id = matches_json['player1_id']
        self._p2_id = matches_json['player2_id']
        self._winner_id = matches_json['winner_id']
        self._loser_id = matches_json['loser_id']
        self._identifier = matches_json['identifier']
        self._round_number = matches_json['round']
        self._round_name = round_names[self.round_number]

        # <nickname, id> map
        self._nicknames = nicknames

        # triggers when initializing matches alone
        if len(nicknames) > 0:
            self._p1_name = nicknames[self._p1_id]
            self._p2_name = nicknames[self._p2_id]
        else:
            self._p1_name = None
            self._p2_name = None

        if matches_json['started_at']:
            self._start_date = matches_json['started_at'].split("T")[0]
            self._start_time = matches_json['started_at'].split("T")[1]
        else:
            # support for underway brackets      
            self._start_date = self._start_time = None

        if matches_json['completed_at']:
            self._finish_date = matches_json['completed_at'].split("T")[0]
            self._finish_time = matches_json['completed_at'].split("T")[1]
        else:
            # support for underway brackets 
            self._finish_date = self._finish_time = None
            
    def __str__(self):
        if len(self._nicknames) > 0:
            return "[{}, {} {} {}]".format(
                self.round_name, self.p1_name, self.score, self.p2_name
            )
        else:
            return "[{}, {} {} {}]".format(
                self.round_name, self.p1_id, self.score, self.p2_id
            )

    def __repr__(self):
        return str(self)

    @property
    def id(self):
        return self._id

    @property
    def p1_id(self):
        return self._p1_id

    @property
    def p1_name(self):
        return self._p1_name

    @property
    def p1_score(self):
        return self._p1_score

    @property
    def p2_id(self):
        return self._p2_id

    @property
    def p2_name(self):
        return self._p2_name

    @property
    def p2_score(self):
        return self._p2_score

    @property
    def winner_id(self):
        return self._winner_id

    @property
    def loser_id(self):
        return self._loser_id

    @property
    def score(self):
        return self._score

    @property
    def identifier(self):
        return self._identifier

    @property
    def round_number(self):
        return self._round_number

    @property
    def round_name(self):
        return self._round_name

    @round_name.setter
    def round_name(self, new_name):
        self._round_name = new_name

    @property
    def start_date(self):
        return self._start_date

    @property
    def start_time(self):
        return self._start_time

    @property
    def finish_date(self):
        return self._finish_date

    @property
    def finish_time(self):
        return self._finish_time

# "players" is a participants list that is used to fetch players' names
def init_matches(url, community='', players=None, tournament_type=None):
    # formats URLs accordingly
    if community != None:
        api_url = f"{TOURNAMENT_URL}{community}{'-'}{url}{'/matches.json'}"
    else:
        api_url = f"{TOURNAMENT_URL}{url}{'/matches.json'}"

    # retrieves raw_data
    raw_matches = fetch_raw_data(api_url)

    # creates a <round num, round name> map and returns it
    round_names = assign_round_names(raw_matches)

    # declaring it here because scope
    output_matches = []

    # fills up nicknames map and creates ChallongeMatch object
    for i in range(0, len(raw_matches)):
        p1_id = raw_matches[i]['match']['player1_id']
        p2_id = raw_matches[i]['match']['player2_id']

        # <id, nickname> map
        nicknames = {}
        if players != None:
            nicknames[p1_id] = get_player_name(p1_id, players)
            nicknames[p2_id] = get_player_name(p2_id, players)

        output_matches.append(ChallongeMatch(
            raw_matches[i]['match'], 
            nicknames, round_names)
        )
    
    # if a reset happens, changes the last set's name
    if output_matches[-1].round_number == output_matches[-2].round_number:
        output_matches[-1].round_name = "Grand Final Reset"
        output_matches[-2].round_name = "Grand Final"

    return output_matches
