import random
from typing import Protocol

from helix.models import Term


class GameMode(Protocol):
    def set_terms(self, terms: list[Term]) -> None: ...

    def next_question(self) -> tuple[Term, ...]: ...


class WriteTheAnswerGameMode:
    def __init__(self) -> None:
        self.terms = None

    def set_terms(self, terms: list[Term]) -> None:
        self.terms = terms

    def next_question(self) -> tuple[Term, ...]:
        if self.terms is None:
            msg = "Terms are not set"
            raise ValueError(msg)

        selected = random.choice(self.terms)  # noqa: S311
        self.terms.pop(self.terms.index(selected))

        return (selected,)


class MultiChoiceGameMode: ...


class ConnectTheDefinitionsGameMode: ...
