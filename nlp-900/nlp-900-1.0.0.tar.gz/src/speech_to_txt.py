"""Module pour transformer de l'audio en texte"""
import speech_recognition as sr
from langdetect import detect


def speech_to_text(audio=None):
    """
    Transforme un contenu audio en texte.

    :param str audio: chemin du fichier audio si audio = None prends le micro comme entrée
    :return: le contenu du fichiers retranscrit en string
    :rtype: str
    """
    r = sr.Recognizer()
    if audio is None:
        with sr.Microphone() as source:
            print("Dites quelque chose!")
            audio = r.listen(source)
    else:
        with sr.AudioFile(audio) as source:
            audio = r.record(source)  # read the entire audio file
    try:
        voice = r.recognize_google(audio, language="fr-FR")
    except sr.UnknownValueError:
        return ""
    if detect(voice) != "fr":
        return ""
    else:
        return voice
