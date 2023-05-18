from pydantic import BaseModel


class CreateCurrency(BaseModel):
    price: float
    currency: str


class UpdateCurrency(BaseModel):
    id: int
    price: float
    currency: str
