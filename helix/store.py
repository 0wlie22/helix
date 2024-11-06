"""Module for storing and managing data in a SQLite database.

Classes:
    Store: Main class for managing data in the database.
    UsersStore: Class for managing users in the database.
    TermGroupsStore: Class for managing term groups in the database.
    TermsStore: Class for managing terms in the database.

Examples:
    # Create a store and manage users
    store = Store("database.db")

    # Operations on users
    user = User(username="user")
    user = store.users.create(user)
    users = store.users.list()
    user = store.users.get(user.id)
    store.users.update(user)
    store.users.delete(user.id)

    # Operations on term groups
    group = TermGroup(name="group", user_id=user.id)
    group = store.term_groups.create(group)
    groups = store.term_groups.list()
    group = store.term_groups.get(group.id)
    store.term_groups.update(group)
    store.term_groups.delete(group.id)

    # Operations on terms
    term = Term(term="term", definition="definition", group_id=group.id)
    term = store.terms.create(term)
    terms = store.terms.list()
    term = store.terms.get(term.id)
    store.terms.update(term)
    store.terms.delete(term.id)

    # Operations on points
    point = Point(points=0, user_id=user.id)
    point = store.points.create(point)
    points = store.points.list()
    point = store.points.get(point.id)
    store.points.update(point)
    store.points.delete(point.id)

"""

import sqlite3

from helix.exceptions import EntityNotFoundError
from helix.models import Point, Term, TermGroup, User


class Store:
    """Store class implements the main interface for managing data in the database."""

    def __init__(self, database: str) -> None:
        self._db = sqlite3.connect(database)

        self.users = UsersStore(self._db)
        self.term_groups = TermGroupsStore(self._db)
        self.terms = TermsStore(self._db)
        self.points = PointsStore(self._db)


class UsersStore:
    """Class for managing users in the database."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self._db = db
        self._create_table()

    def _create_table(self) -> None:
        self._db.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(64) UNIQUE
        )""")

    def create(self, user: User) -> User:
        """Create a new user in the database.

        Args:
            user (User): The user object containing the information of the user to create.

        Returns:
            User: The user object with the assigned ID after creation.
        """
        cur = self._db.cursor()
        cur.execute("INSERT INTO users (username) VALUES (?)", (user.username,))
        user.id = cur.lastrowid
        cur.close()

        return user

    def get_all(self) -> list[User]:
        """Retrieve a list of all users from the database.

        Returns:
            list[User]: A list of user objects representing all users in the database.
        """
        res = self._db.execute("SELECT id, username FROM users")

        return [User(id=row[0], username=row[1]) for row in res.fetchall()]

    def get(self, user_id: int | None) -> User:
        """Retrieve a user from the database by their user ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The user object corresponding to the given user ID.

        Raises:
            ValueError: If the user ID is not set.
            EntityNotFoundError: If no user with the given ID is found.
        """
        if user_id is None:
            msg = "User ID is not set"
            raise ValueError(msg)

        res = self._db.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))

        if row := res.fetchone():
            return User(id=row[0], username=row[1])

        raise EntityNotFoundError

    def get_by_username(self, username: str) -> User:
        """Retrieve a user from the database by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The user object corresponding to the given username.

        Raises:
            EntityNotFoundError: If no user with the given username is found.
        """
        res = self._db.execute("SELECT id, username FROM users WHERE username = ?", (username,))
        row = res.fetchone()

        if row := res.fetchone():
            return User(id=row[0], username=row[1])

        raise EntityNotFoundError

    def update(self, user: User) -> None:
        """Update the username of an existing user in the database.

        Args:
            user (User): The user object containing the updated information.

        Returns:
            None
        """
        self._db.execute("UPDATE users SET username = ? WHERE id = ?", (user.username, user.id))

    def delete(self, user_id: int | None) -> None:
        """Delete a user from the database by their user ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            None
        """
        if user_id is None:
            msg = "User ID is not set"
            raise ValueError(msg)

        self._db.execute("DELETE FROM users WHERE id = ?", (user_id,))


class TermGroupsStore:
    """Class for managing term groups in the database."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self._db = db
        self._create_table()

    def _create_table(self) -> None:
        self._db.execute("""CREATE TABLE IF NOT EXISTS term_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name VARCHAR(64) UNIQUE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )""")

    def create(self, group: TermGroup) -> TermGroup:
        """Create a new TermGroup in the database.

        Args:
            group (TermGroup): The TermGroup object to be created.

        Returns:
            TermGroup: The created TermGroup object with the assigned ID.
        """
        cur = self._db.cursor()
        cur.execute("INSERT INTO term_groups (name, user_id) VALUES (?, ?)", (group.name, group.user_id))
        group.id = cur.lastrowid
        cur.close()

        return group

    def get_all(self) -> list[TermGroup]:
        """Retrieve all TermGroups from the database.

        Returns:
            list[TermGroup]: A list of all TermGroup objects in the database.
        """
        res = self._db.execute("SELECT id, user_id, name FROM term_groups")

        return [TermGroup(id=row[0], user_id=row[1], name=row[2]) for row in res.fetchall()]

    def get(self, group_id: int | None) -> TermGroup:
        """Retrieve a TermGroup by its ID.

        Args:
            group_id (int): The ID of the TermGroup to retrieve.

        Returns:
            TermGroup: The TermGroup object with the specified ID.

        Raises:
            ValueError: If the TermGroup ID is not set
            EntityNotFoundError: If no TermGroup with the specified ID is found.
        """
        if group_id is None:
            msg = "TermGroup ID is not set"
            raise ValueError(msg)

        res = self._db.execute("SELECT id, user_id, name FROM term_groups WHERE id = ?", (group_id,))

        if row := res.fetchone():
            return TermGroup(id=row[0], user_id=row[1], name=row[2])

        raise EntityNotFoundError

    def update(self, group: TermGroup) -> None:
        """Update an existing TermGroup in the database.

        Args:
            group (TermGroup): The TermGroup object containing updated data.

        Returns:
            None
        """
        self._db.execute(
            "UPDATE term_groups SET user_id = ?, name = ? WHERE id = ?",
            (group.user_id, group.name, group.id),
        )

    def delete(self, group_id: int | None) -> None:
        """Delete a TermGroup from the database by its ID.

        Args:
            group_id (int): The ID of the TermGroup to delete.

        Returns:
            None

        Raises:
            ValueError: If the TermGroup ID is not set.
        """
        if group_id is None:
            msg = "TermGroup ID is not set"
            raise ValueError(msg)

        self._db.execute("DELETE FROM term_groups WHERE id = ?", (group_id,))


class TermsStore:
    """Class for managing terms in the database."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self._db = db
        self._create_table()

    def _create_table(self) -> None:
        self._db.execute("""CREATE TABLE IF NOT EXISTS terms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            term TEXT,
            definition TEXT,
            mastery_coef INTEGER,
            total_ans INTEGER,
            correct_ans INTEGER,
            FOREIGN KEY (group_id) REFERENCES term_groups(id)
        )""")

    def create(self, term: Term) -> Term:
        """Create a new Term in the database.

        Args:
            term (Term): The Term object to be created.

        Returns:
            Term: The created Term object with the assigned ID.
        """
        cur = self._db.cursor()
        cur.execute(
            "INSERT INTO terms (group_id, term, definition, mastery_coef, total_ans, correct_ans) VALUES (?, ?, ?, ?, ?, ?)",  # noqa: E501
            (term.group_id, term.term, term.definition, term.mastery_coef, term.total_ans, term.correct_ans),
        )
        term.id = cur.lastrowid
        cur.close()

        return term

    def get_all(self) -> list[Term]:
        """Retrieve all Terms from the database.

        Returns:
            list[Term]: A list of all Term objects in the database.
        """
        res = self._db.execute("SELECT id, group_id, term, definition, mastery_coef, total_ans, correct_ans FROM terms")

        return [
            Term(
                id=row[0],
                group_id=row[1],
                term=row[2],
                definition=row[3],
                mastery_coef=row[4],
                total_ans=row[5],
                correct_ans=row[6],
            )
            for row in res.fetchall()
        ]

    def get_all_by_group_id(self, group_id: int | None) -> list[Term]:
        """Retrieve all Terms from the database by their group ID.

        Args:
            group_id (int): The ID of the group whose Terms are to be retrieved.

        Returns:
            list[Term]: A list of Term objects belonging to the specified group.

        Raises:
            ValueError: If the group ID is not set.
        """
        if group_id is None:
            msg = "Group ID is not set"
            raise ValueError(msg)

        res = self._db.execute(
            "SELECT id, group_id, term, definition, mastery_coef, total_ans, correct_ans FROM terms WHERE group_id = ?",
            (group_id,),
        )

        return [
            Term(
                id=row[0],
                group_id=row[1],
                term=row[2],
                definition=row[3],
                mastery_coef=row[4],
                total_ans=row[5],
                correct_ans=row[6],
            )
            for row in res.fetchall()
        ]

    def get(self, term_id: int | None) -> Term:
        """Retrieve a Term by its ID.

        Args:
            term_id (int): The ID of the Term to retrieve.

        Returns:
            Term: The Term object with the specified ID.

        Raises:
            ValueError: If the Term ID is not set.
            EntityNotFoundError: If no Term with the specified ID is found.
        """
        if term_id is None:
            msg = "Term ID is not set"
            raise ValueError(msg)

        res = self._db.execute(
            "SELECT id, group_id, term, definition, mastery_coef, total_ans, correct_ans FROM terms WHERE id = ?",
            (term_id,),
        )

        if row := res.fetchone():
            return Term(
                id=row[0],
                group_id=row[1],
                term=row[2],
                definition=row[3],
                mastery_coef=row[4],
                total_ans=row[5],
                correct_ans=row[6],
            )

        raise EntityNotFoundError

    def update(self, term: Term) -> None:
        """Update an existing Term in the database.

        Args:
            term (Term): The Term object containing updated data.

        Returns:
            None
        """
        self._db.execute(
            "UPDATE terms SET group_id = ?, term = ?, definition = ?, mastery_coef = ?, total_ans = ?, correct_ans = ? WHERE id = ?",  # noqa: E501
            (term.group_id, term.term, term.definition, term.mastery_coef, term.total_ans, term.correct_ans, term.id),
        )

    def delete(self, term_id: int | None) -> None:
        """Delete a Term from the database by its ID.

        Args:
            term_id (int): The ID of the Term to delete.

        Returns:
            None
        """
        if term_id is None:
            msg = "Term ID is not set"
            raise ValueError(msg)

        self._db.execute("DELETE FROM terms WHERE id = ?", (term_id,))


class PointsStore:
    """Class for managing points in the database."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self._db = db
        self._create_table()

    def _create_table(self) -> None:
        self._db.execute("""CREATE TABLE IF NOT EXISTS points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            points INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )""")

    def create(self, point: Point) -> Point:
        """Create a new Point in the database.

        Args:
            point (Point): The Point object to be created.

        Returns:
            Point: The created Point object with the assigned ID.
        """
        cur = self._db.cursor()
        cur.execute("INSERT INTO points (user_id, points) VALUES (?, ?)", (point.user_id, point.points))
        point.id = cur.lastrowid
        cur.close()

        return point

    def get_all(self) -> list[Point]:
        """Retrieve all Points from the database.

        Returns:
            list[Point]: A list of all Point objects in the database.
        """
        res = self._db.execute("SELECT id, user_id, points FROM points")

        return [Point(id=row[0], user_id=row[1], points=row[2]) for row in res.fetchall()]

    def get(self, point_id: int | None) -> Point:
        """Retrieve a Point by its ID.

        Args:
            point_id (int): The ID of the Point to retrieve.

        Returns:
            Point: The Point object with the specified ID.

        Raises:
            ValueError: If the Point ID is not set.
            EntityNotFoundError: If no Point with the specified ID is found.
        """
        if point_id is None:
            msg = "Point ID is not set"
            raise ValueError(msg)

        res = self._db.execute("SELECT id, user_id, points FROM points WHERE id = ?", (point_id,))

        if row := res.fetchone():
            return Point(id=row[0], user_id=row[1], points=row[2])

        raise EntityNotFoundError

    def get_total_by_user_id(self, user_id: int | None) -> int:
        """Retrieve the total points for a user by their ID.

        Args:
            user_id (int): The ID of the user whose total points are to be retrieved.

        Returns:
            int: The total points of the user.

        Raises:
            ValueError: If the user ID is not set.
        """
        if user_id is None:
            msg = "User ID is not set"
            raise ValueError(msg)

        res = self._db.execute("SELECT sum(points) FROM points WHERE user_id = ?", (user_id,))

        return res.fetchone()[0]

    def update(self, point: Point) -> None:
        """Update an existing Point in the database.

        Args:
            point (Point): The Point object containing updated data.

        Returns:
            None
        """
        self._db.execute(
            "UPDATE points SET user_id = ?, points = ? WHERE id = ?", (point.user_id, point.points, point.id)
        )

    def delete(self, point_id: int | None) -> None:
        """Delete a Point from the database by its ID.

        Args:
            point_id (int): The ID of the Point to delete.

        Returns:
            None

        Raises:
            ValueError: If the Point ID is not set.
        """
        if point_id is None:
            msg = "Point ID is not set"
            raise ValueError(msg)

        self._db.execute("DELETE FROM points WHERE id = ?", (point_id,))
