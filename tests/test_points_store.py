import pytest

from helix.models import Point
from helix.store import PointsStore


@pytest.fixture
def store(db):
    return PointsStore(db)


def test_create_point(store):
    point = Point(id=None, user_id=1, points=100)
    created_point = store.create(point)

    assert created_point.id is not None
    assert created_point.user_id == 1
    assert created_point.points == 100


def test_list_points(store):
    point1 = Point(id=None, user_id=1, points=100)
    point2 = Point(id=None, user_id=2, points=200)
    store.create(point1)
    store.create(point2)
    points = store.list()

    assert len(points) == 2
    assert points[0].user_id == 1
    assert points[0].points == 100
    assert points[1].user_id == 2
    assert points[1].points == 200


def test_get_point(store):
    point = Point(id=None, user_id=1, points=100)
    created_point = store.create(point)
    fetched_point = store.get(created_point.id)

    assert fetched_point is not None
    assert fetched_point.id == created_point.id
    assert fetched_point.user_id == 1
    assert fetched_point.points == 100


def test_update_point(store):
    point = Point(id=None, user_id=1, points=100)
    created_point = store.create(point)
    created_point.points = 150
    store.update(created_point)
    updated_point = store.get(created_point.id)

    assert updated_point.points == 150


def test_delete_point(store):
    point = Point(id=None, user_id=1, points=100)
    created_point = store.create(point)
    store.delete(created_point.id)
    deleted_point = store.get(created_point.id)

    assert deleted_point is None
