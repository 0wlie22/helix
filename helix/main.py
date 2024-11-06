from helix.game_mode import WriteTheAnswerGameMode
from helix.quiz import Quiz
from helix.store import Store


def main() -> None:
    store = Store(":memory:")
    quiz = Quiz(store)
    user = "John Doe"

    quiz.set_active_user(user)
    quiz.set_game_mode(WriteTheAnswerGameMode())


if __name__ == "__main__":
    main()
