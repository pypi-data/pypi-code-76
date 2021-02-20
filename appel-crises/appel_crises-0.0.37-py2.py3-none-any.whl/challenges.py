import datetime
import random

from django.core.signing import Signer

from appel_crises.data.challenges import ANSWERS, CHALLENGES_WITH_ID

signer = Signer()
now = datetime.datetime.now()


def check_answer(challenge_id: int, answer: str):
    """Returns true if the real answer of the challend is given"""
    answer = answer.lower().strip()
    true_answers = ANSWERS[challenge_id]
    return any(answer == possible_true_answer for possible_true_answer in true_answers)


def get_challenge_signed_question_id():
    """
    Get a random challenge.

    :return: the signed id of the challenge, and the relative question
    """
    challenge_id, question, answer = random.choice(CHALLENGES_WITH_ID)
    return signer.sign(challenge_id), question


def check_answer_from_signed_challenge_id(signed_challenge_id: str, answer: str):
    """
    Check if the answer is correct for the given challenge.

    :param signed_challenge_id: the encrypted challenge id
    :param answer: what the user has answered
    """
    challenge_id = int(signer.unsign(signed_challenge_id))
    return check_answer(challenge_id, answer)
