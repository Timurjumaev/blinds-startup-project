from datetime import date
from pydantic import BaseModel


class UpdateLoan(BaseModel):
    id: int
    return_date: date
    comment: str

