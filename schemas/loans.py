from datetime import date
from pydantic import BaseModel


class CreateLoan(BaseModel):
    money: float
    currency_id: int
    order_id: int
    return_date: date
    comment: str


class UpdateLoan(BaseModel):
    id: int
    currency_id: int
    residual: float
    order_id: int
    return_date: date
    comment: str

