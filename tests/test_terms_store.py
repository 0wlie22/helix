import pytest

from helix.models import Term
from helix.store import TermsStore


@pytest.fixture
def store(db):
    return TermsStore(db)


def test_create_term(store):
    term = Term(
        id=None,
        group_id=1,
        word="Test Term",
        definition="Test Definition",
        mastery_coef=0,
        total_ans=0,
        correct_ans=0,
    )
    created_term = store.create(term)

    assert created_term.id is not None
    assert created_term.term == "Test Term"
    assert created_term.definition == "Test Definition"
    assert created_term.group_id == 1


def test_list_terms(store):
    term1 = Term(
        id=None,
        group_id=1,
        word="Term 1",
        definition="Definition 1",
        mastery_coef=0,
        total_ans=0,
        correct_ans=0,
    )
    term2 = Term(
        id=None,
        group_id=2,
        word="Term 2",
        definition="Definition 2",
        mastery_coef=0,
        total_ans=0,
        correct_ans=0,
    )
    store.create(term1)
    store.create(term2)
    terms = store.list()

    assert len(terms) == 2
    assert terms[0].term == "Term 1"
    assert terms[1].term == "Term 2"


def test_get_term(store):
    term = Term(
        id=None,
        group_id=1,
        word="Test Term",
        definition="Test Definition",
        mastery_coef=0,
        total_ans=0,
        correct_ans=0,
    )
    created_term = store.create(term)
    fetched_term = store.get(created_term.id)

    assert fetched_term is not None
    assert fetched_term.id == created_term.id
    assert fetched_term.term == "Test Term"


def test_update_term(store):
    term = Term(
        id=None,
        group_id=1,
        word="Test Term",
        definition="Test Definition",
        mastery_coef=0,
        total_ans=0,
        correct_ans=0,
    )
    created_term = store.create(term)
    created_term.term = "Updated Term"
    store.update(created_term)
    updated_term = store.get(created_term.id)

    assert updated_term.term == "Updated Term"


def test_delete_term(store):
    term = Term(
        id=None,
        group_id=1,
        word="Test Term",
        definition="Test Definition",
        mastery_coef=0,
        total_ans=0,
        correct_ans=0,
    )
    created_term = store.create(term)
    store.delete(created_term.id)
    deleted_term = store.get(created_term.id)

    assert deleted_term is None
