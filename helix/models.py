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

    def update_stats(self, *, correct: bool) -> None:
        """Update the term statistics based on the correctness of an answer.

        Args:
            correct (bool): A boolean indicating whether the answer was correct.

        Returns:
            None
        """
        if correct:
            self.correct_ans += 1

        self.total_ans += 1
        self.update_mastery_coef()

    def update_mastery_coef(self) -> None:
        """Update the mastery coefficient of the Term.

        The mastery coefficient is calculated as the ratio of correct answers to total answers.

        Returns:
            None
        """
        self.mastery_coef = self.correct_ans / self.total_ans


@dataclass
class Point:
    points: int
    user_id: int | None
    id: int | None = None
