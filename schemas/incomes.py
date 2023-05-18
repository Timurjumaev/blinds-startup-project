from pydantic import BaseModel


class CreateIncome(BaseModel):
    money: float
    currency_id: int
    source: str
    source_id: int
    kassa_id: int
    comment: str


class UpdateIncome(BaseModel):
    id: int
    money: float
    currency_id: int
    source: str
    source_id: int
    kassa_id: int
    comment: str

