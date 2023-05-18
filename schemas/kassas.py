from pydantic import BaseModel


class CreateKassa(BaseModel):
    name: str
    comment: str
    balance: float
    currency_id: int


class UpdateKassa(BaseModel):
    id: int
    name: str
    comment: str
    balance: float
    currency_id: int



