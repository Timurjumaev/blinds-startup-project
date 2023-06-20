from typing import List

from pydantic import BaseModel

from schemas.phones import CreatePhone, UpdatePhone


class CreateBranch(BaseModel):
    name: str
    address: str
    map_long: str
    map_lat: str
    phones: List[CreatePhone]


class UpdateBranch(BaseModel):
    id: int
    name: str
    address: str
    map_long: str
    map_lat: str
    phones: List[UpdatePhone]