"""cli"""
import os
import sys

import click
from gtts import gTTS
from playsound import playsound

from src.speech_to_txt import speech_to_text
from src.trip import trip

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("phrase", required=False)
@click.option(
    "--output",
    "-o",
    help="Type d'ouput voulu, raw pour un fichier audio, voice pour un message automatique, et stdout pour des print.(Default = stdout)",
    type=click.Choice(
        ["raw", "stdout", "voice"],
        case_sensitive=False,
    ),
    default="stdout",
)
@click.option(
    "--input",
    "-i",
    help="Type d'input voulu, raw pour des fichiers audio,voice pour le micro, et stdin pour une phrase prise en argument.(Default = stdin)",
    type=click.Choice(
        ["raw", "stdin", "voice"],
        case_sensitive=False,
    ),
    default="stdin",
)
@click.option(
    "--file",
    "-f",
    help="chemin du fichier audio",
    type=click.Path(exists=True),
)
@click.option(
    "--escale",
    "-e",
    help="Nombre d'escales maximum à ne pas dépasser.(Default = 2)",
    type=int,
    default=2,
)
@click.option(
    "--verbose",
    "-vv",
    help="Affiche les messages de debug.",
    is_flag=True,
)
@click.version_option("1.0.0")
def cli(phrase, **kwargs):
    """Method."""
    # input
    if kwargs["input"] == "raw":
        if kwargs["file"] is None:
            click.echo(
                "Utilisez l'option --file pour préciser votre fichier wav.",
            )
            sys.exit(-1)
        sentence = speech_to_text(kwargs["file"])
    elif kwargs["input"] == "stdin" and phrase is not None:
        sentence = phrase
    elif kwargs["input"] == "voice":
        sentence = speech_to_text()
        if kwargs["verbose"]:
            print(f"SpeechRecognizon: {sentence}")
        if sentence == "":
            print("Erreur de compréhension")
    else:
        sys.exit("Input Introuvable.")

    response = trip(sentence, kwargs["escale"], kwargs["verbose"])

    # output
    if kwargs["verbose"]:
        print(f"réponse: {response}")
    if kwargs["output"] == "raw":
        tts = gTTS(text=response, lang="fr")
        tts.save("output.wav")
    elif kwargs["output"] == "voice":
        tts = gTTS(text=response, lang="fr")
        tts.save("output.wav")
        playsound("output.wav")
        os.remove("output.wav")
    elif kwargs["output"] == "stdout":
        print(response)


if __name__ == "__main__":
    cli()
