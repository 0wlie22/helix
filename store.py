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

from models import Point, Term, TermGroup, User


class Store:
    """Store class implements the main interface for managing data in the database."""

    def __init__(self, database: str) -> None:
        self._db = sqlite3.connect(database, autocommit=True)

        self.users = UsersStore(self._db)
        self.term_groups = TermGroupsStore(self._db)
        self.terms = TermsStore(self._db)


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
        cur = self._db.cursor()
        cur.execute("INSERT INTO users (username) VALUES (?)", (user.username,))
        user.id = cur.lastrowid
        cur.close()

        return user

    def list(self) -> list[User]:
        res = self._db.execute("SELECT id, username FROM users")

        users: list[User] = []
        for row in res.fetchall():
            users.append(User(id=row[0], username=row[1]))

        return users

    def get(self, user_id: int) -> User | None:
        res = self._db.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
        row = res.fetchone()

        if row:
            return User(id=row[0], username=row[1])
        return None

    def update(self, user: User) -> None:
        self._db.execute("UPDATE users SET username = ? WHERE id = ?", (user.username, user.id))

    def delete(self, user_id: int) -> None:
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
        cur = self._db.cursor()
        cur.execute("INSERT INTO term_groups (name, user_id) VALUES (?, ?)", (group.name, group.user_id))
        group.id = cur.lastrowid
        cur.close()

        return group

    def list(self) -> list[TermGroup]:
        res = self._db.execute("SELECT id, user_id, name FROM term_groups")

        groups: list[TermGroup] = []
        for row in res.fetchall():
            groups.append(TermGroup(id=row[0], user_id=row[1], name=row[2]))

        return groups

    def get(self, group_id: int) -> TermGroup | None:
        res = self._db.execute("SELECT id, user_id, name FROM term_groups WHERE id = ?", (group_id,))
        row = res.fetchone()

        if row:
            return TermGroup(id=row[0], user_id=row[1], name=row[2])
        return None

    def update(self, group: TermGroup) -> None:
        self._db.execute(
            "UPDATE term_groups SET user_id = ?, name = ? WHERE id = ?",
            (group.user_id, group.name, group.id),
        )

    def delete(self, group_id: int) -> None:
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
        cur = self._db.cursor()
        cur.execute(
            "INSERT INTO terms (group_id, term, definition, mastery_coef, total_ans, correct_ans) VALUES (?, ?, ?, ?, ?, ?)",
            (term.group_id, term.term, term.definition, term.mastery_coef, term.total_ans, term.correct_ans),
        )
        term.id = cur.lastrowid
        cur.close()

        return term

    def list(self) -> list[Term]:
        res = self._db.execute("SELECT id, group_id, term, definition, mastery_coef, total_ans, correct_ans FROM terms")

        terms: list[Term] = []
        for row in res.fetchall():
            terms.append(
                Term(
                    id=row[0],
                    group_id=row[1],
                    term=row[2],
                    definition=row[3],
                    mastery_coef=row[4],
                    total_ans=row[5],
                    correct_ans=row[6],
                )
            )

        return terms

    def get(self, term_id: int) -> Term | None:
        res = self._db.execute(
            "SELECT id, group_id, term, definition, mastery_coef, total_ans, correct_ans FROM terms WHERE id = ?",
            (term_id,),
        )
        row = res.fetchone()

        if row:
            return Term(
                id=row[0],
                group_id=row[1],
                term=row[2],
                definition=row[3],
                mastery_coef=row[4],
                total_ans=row[5],
                correct_ans=row[6],
            )
        return None

    def update(self, term: Term) -> None:
        self._db.execute(
            "UPDATE terms SET group_id = ?, term = ?, definition = ?, mastery_coef = ?, total_ans = ?, correct_ans = ? WHERE id = ?",
            (term.group_id, term.term, term.definition, term.mastery_coef, term.total_ans, term.correct_ans, term.id),
        )

    def delete(self, term_id: int) -> None:
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
        cur = self._db.cursor()
        cur.execute("INSERT INTO points (user_id, points) VALUES (?, ?)", (point.user_id, point.points))
        point.id = cur.lastrowid
        cur.close()

        return point

    def list(self) -> list[Point]:
        res = self._db.execute("SELECT id, user_id, points FROM points")

        points: list[Point] = []
        for row in res.fetchall():
            points.append(Point(id=row[0], user_id=row[1], points=row[2]))

        return points

    def get(self, point_id: int) -> Point | None:
        res = self._db.execute("SELECT id, user_id, points FROM points WHERE id = ?", (point_id,))
        row = res.fetchone()

        if row:
            return Point(id=row[0], user_id=row[1], points=row[2])
        return None

    def update(self, point: Point) -> None:
        self._db.execute(
            "UPDATE points SET user_id = ?, points = ? WHERE id = ?", (point.user_id, point.points, point.id)
        )

    def delete(self, point_id: int) -> None:
        self._db.execute("DELETE FROM points WHERE id = ?", (point_id,))
