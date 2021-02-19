import json

from pkg_resources import resource_stream as rs

from src.Job import Job
from src.Candidate import Candidate


def run_matcher(job: Job) -> [Candidate]:
    """
    search matching Candidate for given Job
    :param job: Job object for search criteria
    """
    candidates_list = __extract_json()['candidates']
    job_skills_list = job.skills.get_list()
    qualified_candidates = list(filter(lambda candidate: job.title.lower() in candidate['title'].lower()
                                and set(job_skills_list).issubset(set(map(str.lower, candidate['skills']))),
                                candidates_list))
    return __build_candidates(qualified_candidates=qualified_candidates)


def __extract_json():
    """ Private method for extracting 'Database' JSON"""
    json_string = rs("src.resources", "database.json").read().decode()
    loaded_json = json.loads(json_string)
    return loaded_json


def __build_candidates(qualified_candidates):
    """ Build Candidate object per dict object from Database"""
    return [Candidate(**candidate) for candidate in qualified_candidates]
