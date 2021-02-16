import pytest

from behalearn.preprocessing import interpolate_custom_event
from behalearn.preprocessing import trapezoid_diagonal_intersection


@pytest.mark.parametrize(
    'prev_event,following_event,custom_event_timestamp,custom_event_coord', [
        ((1, 4, 5), (3, 6, 15), 10, (2, 5)),
        ((1, 4, 5, 5), (3, 6, 7, 15), 10, (2, 5, 6)),
        ((1, 4, 9), (3, 6, 10), 9.5, (2, 5)),
        ((1, 4, 9), (4, 7, 12), 11, (3, 6)),
        ((1, 4, 9), (4, 7, 12), 10, (2, 5)),
        ((1, 4, 9), (5, 8, 10), 9.75, (4, 7)),
        pytest.param(
            (1, 4, 5), (3, 6, 15), 5, (1, 4), id='custom_event_at_start'),
        pytest.param(
            (1, 4, 5), (3, 6, 15), 15, (3, 6), id='custom_event_at_end'),
        pytest.param(
            (1, 4, 5), (3, 6, 5), 5, (2, 5),
            id='zero_timestamp_difference_returns_midpoint'),
    ]
)
def test_interpolate_custom_event(
        prev_event,
        following_event,
        custom_event_timestamp,
        custom_event_coord):
    interpolated_coords = interpolate_custom_event(
        prev_event, following_event, custom_event_timestamp)

    assert interpolated_coords == custom_event_coord


@pytest.mark.parametrize(
    'prev_event,following_event,custom_event_timestamp,custom_event_coord', [
        ((1, 4, 5), (3, 6, 15), 20, (2, 5)),
        ((1, 4, 5), (3, 6, 15), 4, (2, 5)),
    ]
)
def test_interpolate_custom_event_custom_timestamp_out_of_bounds(
        prev_event,
        following_event,
        custom_event_timestamp,
        custom_event_coord):
    with pytest.raises(ValueError):
        interpolate_custom_event(
            prev_event, following_event, custom_event_timestamp)

@pytest.mark.parametrize('points,expected_point', [
    (
        [(15.9, -2.1), (15.9, 5.2), (10.1, 3.6), (10.1, 1.2)],
        (11.53, 2.18),
    ),
    pytest.param(
        [(15.9, -2.1), (15.9, 5.2), (10.1, 9.6), (10.1, 7.2)],
        (11.53, 6.7),
        id='obtuse_trapezoid',
    ),
    pytest.param(
        [(10.1, 3.6), (10.1, 1.2), (15.9, -2.1), (15.9, 5.2)],
        (11.53, 2.18),
        id='first_pair_x_less_than_second',
    ),
    pytest.param(
        [(15.9, 5.2), (15.9, -2.1), (10.1, 3.6), (10.1, 1.2)],
        (11.53, 2.18),
        id='first_coord_y_greater_than_second',
    ),
    pytest.param(
        [(15.9, -2.1), (15.9, 5.2), (10.1, 1.2), (10.1, 3.6)],
        (11.53, 2.18),
        id='third_coord_y_less_than_fourth',
    ),
    pytest.param(
        [(15, 1), (15, 5), (10, 5), (10, 1)],
        (12.5, 3),
        id='rectangle',
    ),
    pytest.param(
        [(15, 5), (15, 6), (15, 4), (15, 1)],
        (15, 4.75),
        id='all_identical_x',
    ),
    pytest.param(
        [(15, 5), (15, 5), (15, 7), (15, 1)],
        (15, 5),
        id='all_identical_x_with_one_pair',
    ),
    pytest.param(
        [(15, 5), (15, 5), (15, 1), (15, 1)],
        (15, 3),
        id='pairs_with_identical_x',
    ),
    pytest.param(
        [(15, 1), (15, 1), (10, 1), (10, 1)],
        (12.5, 1),
        id='pairs_with_identical_y',
    ),
    pytest.param(
        [(15, 1), (15, 1), (15, 1), (15, 1)],
        (15, 1),
        id='all_identical_x_y',
    ),
])
def test_trapezoid_diagonal_intersection(points, expected_point):
    x, y = trapezoid_diagonal_intersection(*points)
    assert (x, y) == pytest.approx(expected_point, abs=0.01)


def test_trapezoid_diagonal_intersection_not_a_trapezoid():
    points = [(14, -2), (15, 5), (10, 3), (11, 1)]
    with pytest.raises(ValueError):
        trapezoid_diagonal_intersection(*points)
