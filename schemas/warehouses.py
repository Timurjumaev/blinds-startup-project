from typing import List

from pydantic import BaseModel

from schemas.phones import CreatePhone, UpdatePhone


class CreateWarehouse(BaseModel):
    name: str
    address: str
    map_long: str
    map_lat: str
    phones: List[CreatePhone]



class UpdateWarehouse(BaseModel):
    id: int
    name: str
    address: str
    map_long: str
    map_lat: str
    phones: List[UpdatePhone]
