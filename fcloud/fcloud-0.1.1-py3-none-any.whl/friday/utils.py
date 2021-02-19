import wikipedia
import requests
from .dictionary import questions

def get_data_from_wiki(cmd: str) -> str:
    title = cmd
    for qn in questions:
        title = title.replace(qn, "").strip()
    title = title.replace(" ?", "").replace("?", "")
    try:
        reply = wikipedia.summary(cmd, sentences=2)
    except wikipedia.exceptions.DisambiguationError:
        reply = 'Sorry sir, Which {} are you refering to ?'.format(title.capitalize())
    except wikipedia.exceptions.PageError:
        reply = "Sorry sir, I don't know much about {}".format(title.capitalize())
    except requests.exceptions.ConnectionError:
        reply = "Maybe if I had a good internet connection, I could answer it."

    return reply
