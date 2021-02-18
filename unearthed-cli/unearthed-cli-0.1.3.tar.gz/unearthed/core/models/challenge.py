"""Unearthed Challenge model."""
import json
import logging
from uuid import UUID

import requests
from unearthed.cli.auth import auth_handler
from unearthed.cli.config import LAMBDA_URL

CHALLENGE_FILENAME = ".unearthed_challenge.json"

logger = logging.getLogger(__name__)


class Challenge:
    """An Unearthed Challenge."""

    _logger = logging.getLogger(__name__)
    challengeId: UUID
    innovatorPlatformRef: UUID
    name: str
    slug: str
    link: str
    start: str
    end: str
    templateUrl: str
    publicDataUrl: str
    scoringFunctionUrl: str
    dockerImage: str
    dataVersion: str
    createdAt: str
    updatedAt: str

    def __init__(
        self,
        challengeId,
        innovatorPlatformRef,
        name,
        slug,
        link,
        start,
        end,
        templateUrl,
        publicDataUrl,
        scoringFunctionUrl,
        dockerImage,
        dataVersion,
        createdAt,
        updatedAt,
        **kwargs,
    ):
        """Construct Challenge instance from **kwargs."""
        self.challengeId = challengeId
        self.innovatorPlatformRef = innovatorPlatformRef
        self.name = name
        self.slug = slug
        self.link = link
        self.start = start
        self.end = end
        self.templateUrl = templateUrl
        self.publicDataUrl = publicDataUrl
        self.dockerImage = dockerImage
        self.scoringFunctionUrl = scoringFunctionUrl
        self.dataVersion = dataVersion
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    def save(self, filename=CHALLENGE_FILENAME):
        """Serialize the Challenge to a JSON file."""
        logger.debug(f"saving to {filename}")
        with open(filename, "w") as json_file:
            json.dump(self.__dict__, json_file, indent=2)

    @staticmethod
    def fromJsonFile(filename):
        """Create a Challenge instance from a saved API response."""
        Challenge._logger.debug("fromJsonFile")
        with open(filename, "r") as f:
            challenge_dict = json.load(f)
            return Challenge(**challenge_dict)

    @staticmethod
    def fromApiById(id):
        """Create a Challenge instance from the Crowd ML API by Id."""
        Challenge._logger.debug("fromApiById")
        url = LAMBDA_URL + "challenges/" + id
        response = requests.get(url, auth=auth_handler, timeout=20)
        response.raise_for_status()
        challenge_dict = response.json()["challenge"]
        return Challenge(**challenge_dict)

    @staticmethod
    def allFromApi():
        """Create challenge instances from the Crowd ML API."""
        url = LAMBDA_URL + "challenges/"
        response = requests.get(url, auth=auth_handler, timeout=20)
        response.raise_for_status()
        if "challenges" in response.json():
            challenges = []
            for challenge_dict in response.json()["challenges"]:
                challenges.append(Challenge(**challenge_dict))
            return challenges
        else:
            return []
