import pytest

from helix.exceptions import EntityNotFoundError
from helix.models import Point
from helix.store import PointsStore


@pytest.fixture
def store(db):
    return PointsStore(db)


def test_create_point(store: PointsStore):
    point = Point(id=None, user_id=1, points=100)
    created_point = store.create(point)

    assert created_point.id is not None
    assert created_point.user_id == 1
    assert created_point.points == 100


def test_get_all_points(store: PointsStore):
    point1 = Point(id=None, user_id=1, points=100)
    point2 = Point(id=None, user_id=2, points=200)
    store.create(point1)
    store.create(point2)
    points = store.get_all()

    assert len(points) == 2
    assert points[0].user_id == 1
    assert points[0].points == 100
    assert points[1].user_id == 2
    assert points[1].points == 200


def test_get_point(store: PointsStore):
    point = Point(id=None, user_id=1, points=100)
    created_point = store.create(point)
    fetched_point = store.get(created_point.id)

    assert fetched_point is not None
    assert fetched_point.id == created_point.id
    assert fetched_point.user_id == 1
    assert fetched_point.points == 100


def test_get_point_none_id(store: PointsStore):
    with pytest.raises(ValueError, match="Point ID is not set"):
        store.get(None)


def test_get_point_not_found(store: PointsStore):
    with pytest.raises(EntityNotFoundError):
        store.get(1)


def test_get_total_by_user_id(store: PointsStore):
    point1 = Point(user_id=1, points=100)
    point2 = Point(user_id=1, points=50)
    store.create(point1)
    store.create(point2)

    fetched_points = store.get_total_by_user_id(1)

    assert fetched_points == 150


def test_update_point(store: PointsStore):
    point = Point(id=None, user_id=1, points=100)
    created_point = store.create(point)
    created_point.points = 150
    store.update(created_point)
    updated_point = store.get(created_point.id)

    assert updated_point.points == 150


def test_delete_point(store: PointsStore):
    point = Point(id=None, user_id=1, points=100)
    created_point = store.create(point)
    store.delete(created_point.id)

    with pytest.raises(EntityNotFoundError):
        store.get(created_point.id)


def test_delete_point_none_id(store: PointsStore):
    with pytest.raises(ValueError, match="Point ID is not set"):
        store.delete(None)
