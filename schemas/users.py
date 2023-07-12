from typing import List

from pydantic import BaseModel

from schemas.phones import CreatePhone


class CreateUser(BaseModel):
    name: str
    username: str
    password: str
    role: str
    status: bool
    phones: List[CreatePhone]


class CreateBranchUser(BaseModel):
    name: str
    username: str
    password: str
    role: str
    status: bool
    branch_id: int
    phones: List[CreatePhone]


class UpdateUser(BaseModel):
    id: int
    name: str
    username: str
    password: str
    role: str
    status: bool
    phones: List[CreatePhone]


class TokenUser(BaseModel):
    id: int
    username: str
    role: str
    token: str

