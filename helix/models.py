from dataclasses import dataclass


@dataclass
class User:
    username: str
    id: int | None = None


@dataclass
class TermGroup:
    name: str
    user_id: int | None
    id: int | None = None


@dataclass
class Term:
    term: str
    definition: str
    group_id: int | None
    mastery_coef: float = 0.0
    total_ans: int = 0
    correct_ans: int = 0
    id: int | None = None

    def __str__(self) -> str:
        return f"{self.term}: {self.definition}"

    def __iter__(self):
        yield self


@dataclass
class Point:
    points: int
    user_id: int | None
    id: int | None = None
