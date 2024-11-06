# quiz.py

import logging

from helix.exceptions import ActiveUserIsNotSetError, EntityNotFoundError, TermGroupIsNotSetError
from helix.game_mode import GameMode
from helix.models import Point, Term, TermGroup, User
from helix.store import Store


class Quiz:
    def __init__(self, store: Store) -> None:
        self.store = store
        self.score = 0  # Active session score
        self.active_user: User | None = None
        self.term_group: TermGroup | None = None
        self.game_mode: GameMode | None = None

    def set_active_user(self, username: str) -> None:
        """Set the active user for the quiz."""
        try:
            user = self.store.users.get_by_username(username)
        except EntityNotFoundError:
            logging.exception("User %q not found", username)
            return

        self.active_user = user

    def get_active_user(self) -> User:
        if self.active_user is None:
            raise ActiveUserIsNotSetError

        return self.active_user

    def set_term_group(self, group: TermGroup) -> None:
        self.term_group = group

    def set_game_mode(self, mode: GameMode) -> None:
        self.game_mode = mode

    def get_terms(self) -> list[Term]:
        """Retrieve all terms for the quiz."""
        if self.term_group is None:
            raise TermGroupIsNotSetError

        return self.store.terms.get_all_by_group_id(self.term_group.id)

    def check_answer(self, user_answer: str, correct_answer: str) -> bool:
        """Check if the user's answer matches the correct answer."""
        return user_answer.strip().lower() == correct_answer.strip().lower()

    def update_mastery(self, term: Term, *, correct: bool) -> None:
        """Update mastery coefficient and answer counts for the term."""
        term.update_stats(correct=correct)
        self.store.terms.update(term)

    def get_session_score(self) -> int:
        return self.score

    def get_total_score(self) -> int:
        if self.active_user is None:
            raise ActiveUserIsNotSetError

        return self.store.points.get_total_by_user_id(self.active_user.id)

    def add_points(self, amount: int) -> None:
        if self.active_user is None:
            raise ActiveUserIsNotSetError

        self.store.points.create(Point(points=amount, user_id=self.active_user.id))

    def reset(self) -> None:
        self.score = 0
        self.active_user = None
        self.term_group = None
        self.game_mode = None
