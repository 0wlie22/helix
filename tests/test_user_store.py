import pytest

from helix.models import User
from helix.store import UsersStore


@pytest.fixture
def store(db):
    return UsersStore(db)


def test_create_user(store):
    user = User(username="testuser")
    created_user = store.create(user)

    assert created_user.id is not None
    assert created_user.username == "testuser"


def test_list_users(store):
    user1 = User(username="user1")
    user2 = User(username="user2")
    store.create(user1)
    store.create(user2)
    users = store.list()

    assert len(users) == 2
    assert users[0].username == "user1"
    assert users[1].username == "user2"


def test_get_user(store):
    user = User(username="testuser")
    created_user = store.create(user)
    fetched_user = store.get(created_user.id)

    assert fetched_user is not None
    assert fetched_user.username == "testuser"


def test_update_user(store):
    user = User(username="testuser")
    created_user = store.create(user)
    created_user.username = "updateduser"
    store.update(created_user)
    updated_user = store.get(created_user.id)

    assert updated_user.username == "updateduser"


def test_delete_user(store):
    user = User(username="testuser")
    created_user = store.create(user)
    store.delete(created_user.id)
    deleted_user = store.get(created_user.id)

    assert deleted_user is None
