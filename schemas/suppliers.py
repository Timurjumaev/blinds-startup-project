from typing import List

from pydantic import BaseModel

from schemas.phones import CreatePhone, UpdatePhone


class CreateSupplier(BaseModel):
    name: str
    address: str
    map_long: str
    map_lat: str
    phones: List[CreatePhone]


class UpdateSupplier(BaseModel):
    id: int
    name: str
    address: str
    map_long: str
    map_lat: str
    phones: List[UpdatePhone]

