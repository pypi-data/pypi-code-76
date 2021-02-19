import json
import random

import requests

url = 'https://void206551.dev/projects/melody/resources/fun/fun.json'
r = requests.get(url)
data = json.loads(r.text)


def joke():
    # jokeResponse = random.choice(data[0]["joke"])
    return random.choice(data[0]["joke"])


def topic():
    # topicResponse = random.choice(data[0]["topic"])
    return random.choice(data[0]["topic"])


def pickup():
    # pickupResponse = random.choice(data[0]["pickup"])
    return random.choice(data[0]["pickup"])


def roast():
    # roastResponse = random.choice(data[0]["roast"])
    return random.choice(data[0]["roast"])


def toast():
    # toastResponse = random.choice(data[0]["toast"])
    return random.choice(data[0]["toast"])
