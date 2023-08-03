from pydantic import BaseModel


class CreateKassa(BaseModel):
    name: str
    currency_id: int


class UpdateKassa(BaseModel):
    id: int
    name: str


class TransferSchema(BaseModel):
    id1: int
    id2: int
    money: float
    currency_id: int


