from typing import List, Dict
from canvasapi import Canvas
from contextlib import contextmanager
from canvasapi.quiz import QuizSubmissionQuestion, QuizSubmission
from environs import Env
from pset1.hash_str import get_user_id
import pandas as pd

env = Env()
env.read_env()

canvas = Canvas(env("CANVAS_URL"), env("CANVAS_TOKEN"))
user = canvas.get_user(env("CANVAS_USER_ID"))
course_list = user.get_courses()
course = course_list[0]
all_quizzes = course.get_quizzes()
all_assignments = course.get_assignments()
masquerade = {}


def get_course_id(uuid=False):
    """return canvas course id"""
    if uuid:
        return course.uuid
    else:
        canvas_course_id = course.id
        return canvas_course_id


def get_quiz_id(quiz_name='Pset 1 Answers'):
    """return quiz id"""
    quiz_list = list()
    quiz_id_list = list()
    for class_quiz in all_quizzes:
        quiz_list.append(class_quiz.title)
        quiz_id_list.append(class_quiz.id)
    if quiz_name in quiz_list:
        return quiz_id_list[quiz_list.index(quiz_name)]
    else:
        raise NameError("Desired quiz name not found")


def get_assignment_id(assignment_name='Pset 1'):
    """return assignment id"""
    assignment_list = list()
    assignment_id_list = list()
    for class_assignment in all_assignments:
        assignment_list.append(class_assignment.name)
        assignment_id_list.append(class_assignment.id)
    if assignment_name in assignment_list:
        return assignment_id_list[assignment_list.index(assignment_name)]
    else:
        raise NameError("Desired assignment name not found")


def get_excel_user_ids():
    data_source = 'data/hashed.xlsx'
    data_source_df = pd.read_excel(data_source)
    data_source_df = data_source_df.sort_values('hashed_id')
    data_source_df = data_source_df.set_index('hashed_id')
    return data_source_df


def get_questions():
    quiz = course.get_quiz(get_quiz_id(), **masquerade)
    qsubmission = quiz.create_submission(**masquerade)
    questions = qsubmission.get_submission_questions(**masquerade)
    qsubmission.complete(**masquerade)
    return questions


def get_answers(questions: List[QuizSubmissionQuestion]) -> List[Dict]:
    """Creates answers for Canvas quiz questions"""
    # Formulate your answers - see docs for QuizSubmission.answer_submission_questions below
    # It should be a list of dicts, one per q, each with an 'id' and 'answer' field
    # The format of the 'answer' field depends on the question type
    # You are responsible for collating questions with the functions to call - do not hard code
    data_source_df = get_excel_user_ids()
    return [{'id': questions[0].id,
             'answer': {'gorlins': get_user_id('gorlins'),
                        'torvalds': get_user_id('torvalds'),
                        'wesm': get_user_id('wesm')}},
            {'id': questions[1].id,
             'answer': {'u_0': str(data_source_df.index[0]),
                        'u_1': str(data_source_df.index[1]),
                        'u_2': str(data_source_df.index[2]),
                        'u_3': str(data_source_df.index[3]),
                        'u_4': str(data_source_df.index[4])}},
            ]


def get_submission_comments(qsubmission: QuizSubmission) -> Dict:
    """Get some info about this submission"""
    return dict(
        # hexsha=repo.head.commit.hexsha[:8],
        # submitted_from=repo.remotes.origin.url,
        # dt=repo.head.commit.committed_datetime.isoformat(),
        # branch="master",  # repo.active_branch.name,
        # is_dirty=repo.is_dirty(),
        quiz_submission_id=qsubmission.id,
        quiz_attempt=qsubmission.attempt,
        # travis_url="https://travis-ci.com/github/nikhar1210/2021sp-pset-1-nikhar1210/",
    )


@contextmanager
def quiz_submission(course_id, assignment_id, quiz_id, allow_dirty=False):
    """

    :param course_id: course_id for quiz submission
    :param assignment_id: assignment for quiz submission
    :param quiz_id: quiz_id for quiz submission
    :param allow_dirty: allow if repo is not committed
    :return: quiz submission
    """

    # repo = Repo(".")
    #
    # if repo.is_dirty() and not allow_dirty:
    #     raise RuntimeError("Must submit from a clean working directory - commit your code and rerun")

    # Load canvas objects
    assignment = course.get_assignment(assignment_id, **masquerade)
    quiz = course.get_quiz(quiz_id, **masquerade)

    # Begin submissions
    URL = "https://github.com/csci-e-29/"
    # you MUST push to the classroom org, even if CI/CD
    # runs elsewhere (you can push anytime before peer review begins)

    qsubmission = None
    try:
        # Attempt quiz submission first - only submit assignment if successful
        qsubmission = quiz.create_submission(**masquerade)
        questions = qsubmission.get_submission_questions(**masquerade)
        # Submit your answers
        answers = get_answers(questions)
        yield answers
        responses = qsubmission.answer_submission_questions(quiz_questions=answers, **masquerade)

    finally:
        if qsubmission is not None:
            completed = qsubmission.complete(**masquerade)

        #     # Only submit assignment if quiz finished successfully
        #     submission = assignment.submit(
        #         dict(submission_type="online_url",
        #              url=URL,),
        #         comment=dict(text_comment=json.dumps(get_submission_comments(qsubmission))),
        #         **masquerade,
        #     )
