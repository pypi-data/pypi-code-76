"""Unearthed Sumission Entity."""
import json
import logging
from uuid import UUID

import requests
from unearthed.cli.auth import auth_handler
from unearthed.cli.config import LAMBDA_URL

_LAST_SUBMISSION_FILENAME = '.unearthed_last_submission.json'


class Submission():
    """A submission to an Unearthed challenge."""

    _logger = logging.getLogger(__name__)
    submissionId: UUID
    challengeRef: UUID
    userRef: UUID
    teamRef: UUID
    status: str
    createdAt: str
    updatedAt: str
    sourceUploadUrl: str
    configUploadUrl: str
    innovatorPortalSubmissionRef: UUID

    def __init__(self,
                 submissionId,
                 challengeRef,
                 userRef,
                 teamRef,
                 status,
                 createdAt,
                 updatedAt,
                 sourceUploadUrl,
                 configUploadUrl,
                 innovatorPortalSubmissionRef):
        self.submissionId = submissionId
        self.challengeRef = challengeRef
        self.userRef = userRef
        self.teamRef = teamRef
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.sourceUploadUrl = sourceUploadUrl
        self.configUploadUrl = configUploadUrl
        self.innovatorPortalSubmissionRef = innovatorPortalSubmissionRef

    @staticmethod
    def fromJsonFile(filename):
        """Create a Submission isntance from a saved API response."""
        with open(filename, 'r') as f:
            submission_dict = json.load(f)
            return Submission(**submission_dict)

    @staticmethod
    def fromApi(challengeId):
        """Create a Submission instance from the Crowd ML API."""
        Submission._logger.debug('fromApi')
        url = LAMBDA_URL + f'challenges/{challengeId}/submission'
        Submission._logger.debug(f'posting to {url}')
        response = requests.post(url=url, auth=auth_handler, timeout=10)
        response.raise_for_status()
        submission_dict = response.json()['submission']
        submission_dict['sourceUploadUrl'] = response.json()['sourceUploadUrl']
        submission_dict['innovatorPortalSubmissionRef'] = response.json()['innovatorPortalSubmissionRef']
        submission_dict['configUploadUrl'] = response.json()['configUploadUrl']
        submission = Submission(**submission_dict)
        Submission._save(submission_dict)
        return submission

    @staticmethod
    def _save(submission_dict):
        """Save the Submission to disk."""
        with open(_LAST_SUBMISSION_FILENAME, 'w') as json_file:
            json.dump(submission_dict, json_file, indent=2)
