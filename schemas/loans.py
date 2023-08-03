from datetime import date
from pydantic import BaseModel


# class CreateLoan(BaseModel):
#     order_id: int
#     return_date: date
#     comment: str


class UpdateLoan(BaseModel):
    id: int
    return_date: date
    comment: str

