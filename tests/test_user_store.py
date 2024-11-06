import pytest

from helix.exceptions import EntityNotFoundError
from helix.models import User
from helix.store import UsersStore


@pytest.fixture
def store(db) -> UsersStore:
    return UsersStore(db)


def test_create_user(store: UsersStore):
    user = User(username="testuser")
    created_user = store.create(user)

    assert created_user.id is not None
    assert created_user.username == "testuser"


def test_get_all_users(store: UsersStore):
    user1 = User(username="user1")
    user2 = User(username="user2")
    store.create(user1)
    store.create(user2)
    users = store.get_all()

    assert len(users) == 2
    assert users[0].username == "user1"
    assert users[1].username == "user2"


def test_get_user(store: UsersStore):
    user = User(username="testuser")
    created_user = store.create(user)
    fetched_user = store.get(created_user.id)

    assert fetched_user is not None
    assert fetched_user.username == "testuser"


def test_get_user_none_id(store: UsersStore):
    with pytest.raises(ValueError, match="User ID is not set"):
        store.get(None)


def test_get_user_not_found(store: UsersStore):
    with pytest.raises(EntityNotFoundError):
        store.get(1)


def test_update_user(store: UsersStore):
    user = User(username="testuser")
    created_user = store.create(user)
    created_user.username = "updateduser"
    store.update(created_user)
    updated_user = store.get(created_user.id)

    assert updated_user.username == "updateduser"


def test_delete_user(store: UsersStore):
    user = User(username="testuser")
    created_user = store.create(user)
    store.delete(created_user.id)

    with pytest.raises(EntityNotFoundError):
        store.get(created_user.id)


def test_delete_user_none_id(store: UsersStore):
    with pytest.raises(ValueError, match="User ID is not set"):
        store.delete(None)
