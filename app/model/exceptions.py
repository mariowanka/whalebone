from typing import Any


class ModelException(Exception):
    def __init__(self, context: Any):
        self.context = context


class UserAlreadyExistsException(ModelException):
    message = "User with given id already exists"
