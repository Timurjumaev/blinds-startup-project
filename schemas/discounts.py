from pydantic import BaseModel


class CreateDiscount(BaseModel):
    type: str
    percent: float


class UpdateDiscount(BaseModel):
    id: int
    type: str
    percent: float
