import pytest

from model_bakery import baker

from huscy.projects.models import Project
from huscy.bookings.services import get_timeslots_for_project

pytestmark = pytest.mark.django_db


def test_get_timeslots_for_project():

    project1 = baker.make(Project)
    project2 = baker.make(Project)
    experiment1, experiment2 = baker.make('projects.Experiment', project=project1, _quantity=2)
    experiment3 = baker.make('projects.Experiment', project=project2)
    session1 = baker.make('projects.Session', experiment=experiment1)
    session2 = baker.make('projects.Session', experiment=experiment2)
    session3 = baker.make('projects.Session', experiment=experiment3)
    baker.make('bookings.Timeslot', session=session1, _quantity=2)
    baker.make('bookings.Timeslot', session=session2)
    baker.make('bookings.Timeslot', session=session3, _quantity=2)

    timeslots = get_timeslots_for_project(project=project1)
    assert len(timeslots) == 3

    timeslots = get_timeslots_for_project(project=project2)
    assert len(timeslots) == 2
