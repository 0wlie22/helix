# main.py

from store import Store
from quiz import Quiz
from models import User, Term, TermGroup

def main():
    print("Hello from HELIX!")

    """
    # Initialize store and user
    store = Store("database.db")
    user = store.users.get(1)  # Assume user ID 1 for the demo
    if not user:
        user = store.users.create(User(username="Demo User"))

    # Create a sample term group
    group = store.term_groups.create(TermGroup(name="Sample Group", user_id=user.id))

    # Check if there are terms in the database, if not, add sample terms
    if not store.terms.list():
        print("No terms found, adding sample terms...")
        sample_terms = [
            Term(term="Python", definition="A programming language.", group_id=group.id),
            Term(term="Database", definition="A place to store data.", group_id=group.id),
            Term(term="Function", definition="A block of code that performs a specific task.", group_id=group.id)
        ]
        for term in sample_terms:
            store.terms.create(term)

    # Start the quiz
    quiz = Quiz(store, user.id)
    quiz.start_quiz()
"""

if __name__ == "__main__":
    main()

