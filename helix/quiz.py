from models import Point, Term
from store import Store


class Quiz:
    def __init__(self, store: Store, user_id: int) -> None:
        self.store = store
        self.user_id = user_id
        self.points = 0  # Track total points for this session

    def get_terms(self) -> list[Term]:
        """Retrieve all terms for the quiz."""
        return self.store.terms.list()

    def check_answer(self, user_answer: str, correct_answer: str) -> bool:
        """Check if the user's answer matches the correct answer."""
        return user_answer.strip().lower() == correct_answer.strip().lower()

    def update_mastery(self, term: Term, *, correct: bool) -> None:
        """Update mastery coefficient and answer counts for the term."""
        term.total_ans += 1
        if correct:
            term.correct_ans += 1
            self.points += 1  # Increment points for correct answers

        # Calculate new mastery coefficient
        term.mastery_coef = term.correct_ans / term.total_ans
        self.store.terms.update(term)  # Save changes to the database

    def update_user_points(self) -> None:
        """Update the user's total points in the database."""
        user_points = self.store.points.get(self.user_id)
        if user_points:
            user_points.points += self.points
            self.store.points.update(user_points)
        else:
            # Create initial points record if it doesn't exist
            self.store.points.create(Point(points=self.points, user_id=self.user_id))

    def start_quiz(self) -> None:
        """Run the quiz session."""
        terms = self.get_terms()
        print("Starting the quiz...")  # noqa: T201

        for term in terms:
            print(f"Define: {term.term}")  # noqa: T201
            user_answer = input("Your answer: ")

            correct = self.check_answer(user_answer, term.definition)
            if correct:
                print("Correct!")  # noqa: T201
            else:
                print(f"Incorrect. The correct answer is: {term.definition}")  # noqa: T201

            self.update_mastery(term, correct=correct)

        # Finalize by updating user points
        self.update_user_points()
        print(f"Quiz finished. You scored {self.points} points in this session.")  # noqa: T201
