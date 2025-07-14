from datetime import datetime
from uuid import UUID

from attrs import define


@define
class User:
    external_id: UUID
    name: str
    email: str
    date_of_birth: datetime
