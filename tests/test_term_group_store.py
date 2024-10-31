import pytest

from helix.models import TermGroup
from helix.store import TermGroupsStore


@pytest.fixture
def store(db):
    return TermGroupsStore(db)


def test_create_group(store):
    group = TermGroup(id=None, user_id=1, name="Test Group")
    created_group = store.create(group)

    assert created_group.id is not None
    assert created_group.name == "Test Group"
    assert created_group.user_id == 1


def test_list_groups(store):
    group1 = TermGroup(id=None, user_id=1, name="Group 1")
    group2 = TermGroup(id=None, user_id=2, name="Group 2")
    store.create(group1)
    store.create(group2)
    groups = store.list()

    assert len(groups) == 2
    assert groups[0].name == "Group 1"
    assert groups[1].name == "Group 2"


def test_get_group(store):
    group = TermGroup(id=None, user_id=1, name="Test Group")
    created_group = store.create(group)
    fetched_group = store.get(created_group.id)

    assert fetched_group is not None
    assert fetched_group.id == created_group.id
    assert fetched_group.name == "Test Group"


def test_update_group(store):
    group = TermGroup(id=None, user_id=1, name="Test Group")
    created_group = store.create(group)
    created_group.name = "Updated Group"
    store.update(created_group)
    updated_group = store.get(created_group.id)

    assert updated_group.name == "Updated Group"


def test_delete_group(store):
    group = TermGroup(id=None, user_id=1, name="Test Group")
    created_group = store.create(group)
    store.delete(created_group.id)
    deleted_group = store.get(created_group.id)

    assert deleted_group is None
