import pytest

from helix.exceptions import EntityNotFoundError
from helix.models import Term
from helix.store import TermsStore


@pytest.fixture
def store(db):
    return TermsStore(db)


def test_create_term(store: TermsStore):
    term = Term(
        id=None,
        group_id=1,
        term="Test Term",
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


def test_get_all_terms(store: TermsStore):
    term1 = Term(
        id=None,
        group_id=1,
        term="Term 1",
        definition="Definition 1",
        mastery_coef=0,
        total_ans=0,
        correct_ans=0,
    )
    term2 = Term(
        id=None,
        group_id=2,
        term="Term 2",
        definition="Definition 2",
        mastery_coef=0,
        total_ans=0,
        correct_ans=0,
    )
    store.create(term1)
    store.create(term2)
    terms = store.get_all()

    assert len(terms) == 2
    assert terms[0].term == "Term 1"
    assert terms[1].term == "Term 2"


def test_get_all_by_group_id(store: TermsStore):
    term1 = Term(
        id=None,
        group_id=1,
        term="Term 1",
        definition="Definition 1",
        mastery_coef=0,
        total_ans=0,
        correct_ans=0,
    )
    term2 = Term(
        id=None,
        group_id=1,
        term="Term 2",
        definition="Definition 2",
        mastery_coef=0,
        total_ans=0,
        correct_ans=0,
    )
    store.create(term1)
    store.create(term2)
    terms = store.get_all_by_group_id(1)

    assert len(terms) == 2
    assert terms[0].term == "Term 1"
    assert terms[1].term == "Term 2"


def test_get_term(store: TermsStore):
    term = Term(
        id=None,
        group_id=1,
        term="Test Term",
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


def test_get_term_none_id(store: TermsStore):
    with pytest.raises(ValueError, match="Term ID is not set"):
        store.get(None)


def test_get_term_not_found(store: TermsStore):
    with pytest.raises(EntityNotFoundError):
        store.get(1)


def test_update_term(store: TermsStore):
    term = Term(
        id=None,
        group_id=1,
        term="Test Term",
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


def test_delete_term(store: TermsStore):
    term = Term(
        id=None,
        group_id=1,
        term="Test Term",
        definition="Test Definition",
        mastery_coef=0,
        total_ans=0,
        correct_ans=0,
    )
    created_term = store.create(term)
    store.delete(created_term.id)

    with pytest.raises(EntityNotFoundError):
        store.get(created_term.id)


def test_delete_term_none_id(store: TermsStore):
    with pytest.raises(ValueError, match="Term ID is not set"):
        store.delete(None)
