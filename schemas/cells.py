from pydantic import BaseModel


class CreateCell(BaseModel):
    name1: str
    name2: str
    warehouse_id: int


class UpdateCell(BaseModel):
    id: int
    name1: str
    name2: str
    warehouse_id: int

