from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy import Engine

from app.infrastructure import Repository
from app.model.exceptions import UserAlreadyExistsException
from app.model.user import User


class TestRepository:
    @pytest.fixture
    def repository(self, engine: Engine) -> Repository:
        return Repository(engine)

    def test_save_new_user(self, repository):
        # setup
        user = User(
            external_id=uuid4(),
            name="foo",
            email="foo@bar.com",
            date_of_birth=datetime.now(),
        )

        # run
        repository.save_user(user)

        # verify
        assert user == repository.get_user(user.remote_id)

    def test_save_user_already_existing(self, repository):
        # setup
        user = User(
            external_id=uuid4(),
            name="foo",
            email="foo@bar.com",
            date_of_birth=datetime.now(),
        )

        # run
        with pytest.raises(UserAlreadyExistsException):
            repository.save_user(user)

    def test_get_user_does_not_exist(self, repository):
        # run
        user = repository.get_user(uuid4())

        # verify
        assert user is None
