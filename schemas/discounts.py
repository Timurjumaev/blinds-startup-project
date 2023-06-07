from pydantic import BaseModel


class CreateDiscount(BaseModel):
    type: str
    percent: float

