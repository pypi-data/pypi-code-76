import requests

TOURNAMENT_URL = "https://api.challonge.com/v1/tournaments/"

# api_key helpers
_api_key = {}
def set_api_key(your_api_key):
    _api_key['api_key'] = your_api_key

def get_api_key():
    return _api_key

# init functions helpers
def fetch_raw_data(api_url):
    api_key = get_api_key()

    if len(api_key['api_key']) < 40:
        raise SystemExit("API key has not been set or is incorrect.")

    response = requests.get(api_url, api_key)

    if not response.ok:
        if response.status_code == (404):
            raise SystemExit("404: please check your input and try again.")
        else:
            raise SystemExit("an error has occurred, please try again.")
    else:
        raw_data = response.json()

    return raw_data

# init_matches() helpers
def get_player_name(id, players):
    for p in players:
        if p.id == id:
            return p.name

def assign_round_names(matches):
    rounds_names = {}

    # round stacks
    losers = ['Losers Eights', 'Losers Eights', 'Losers Quarters', 
        'Losers Quarters', 'Losers Semis', 'Losers Finals']
    winners = ['Winners Semis', 'Winners Semis', 
        'Winners Final', 'Grand Final']

    c = len(matches)
    while (c > 0):
        round_num = matches[c - 1]["match"]["round"]

        # positive rounds are winners rounds
        if round_num > 0:
            if len(winners) > 0:
                rounds_names[round_num] = winners.pop(len(winners) - 1)
            else:
                rounds_names[round_num] = "Winners Round " + str(round_num)
        # losers rounds are negative
        else:
            if len(losers) > 0:
                rounds_names[round_num] = losers.pop(len(losers) - 1)
            else:
                # losers rounds are internally represented as negative ints
                rounds_names[round_num] = "Losers Round " + str(round_num * -1)
        
        c -= 1

    return rounds_names
