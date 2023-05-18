from typing import List

from pydantic import BaseModel

from schemas.phones import CreatePhone, UpdatePhone


class CreateCustomer(BaseModel):
    name: str
    type: str
    phones: List[CreatePhone]


class UpdateCustomer(BaseModel):
    id: int
    name: str
    type: str
    phones: List[UpdatePhone]
