class EntityNotFoundError(Exception):
    """This exception is rised when an entity is not found in the database."""


class ActiveUserIsNotSetError(Exception):
    """This exception is raised when the active user is not set."""


class TermGroupIsNotSetError(Exception):
    """This exception is raised when the term group is not set."""
