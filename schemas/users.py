from typing import List

from pydantic import BaseModel

from schemas.phones import CreatePhone, UpdatePhone


class CreateUser(BaseModel):
    name: str
    username: str
    password: str
    role: str
    status: bool
    phones: List[CreatePhone]


class UpdateUser(BaseModel):
    id: int
    name: str
    username: str
    password: str
    role: str
    status: bool
    phones: List[UpdatePhone]
