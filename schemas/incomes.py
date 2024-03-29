from pydantic import BaseModel


class CreateIncome(BaseModel):
    money: float
    source: str
    source_id: int
    kassa_id: int
    comment: str

