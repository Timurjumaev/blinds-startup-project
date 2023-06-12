from pydantic import BaseModel


class CreateExpense(BaseModel):
    money: float
    currency_id: int
    source: str
    source_id: int
    kassa_id: int
    comment: str
