from uuid import UUID

from sqlalchemy import Engine, MetaData, Table, insert, select
from sqlalchemy.exc import IntegrityError

from app.model.exceptions import UserAlreadyExistsException
from app.model.json import structure, unstructure
from app.model.user import User


class Repository:
    def __init__(self, engine: Engine):
        metadata = MetaData()
        metadata.reflect(bind=engine, only=["users"])

        self._users: Table = metadata.tables["users"]
        self._engine = engine

    def save_user(self, user: User):
        query = insert(self._users).values(unstructure(user))

        with self._engine.connect() as connection:
            try:
                connection.execute(query)
            except IntegrityError:
                raise UserAlreadyExistsException(
                    context={"user": unstructure(user)},
                )

    def get_user(self, user_id: UUID) -> User | None:
        query = select(self._users).where(self._users.c.external_id == user_id)
        with self._engine.connect() as connection:
            if (row := connection.execute(query).fetchone()) is None:
                return None

            return structure(row._mapping, User)
