from pydantic import BaseModel


class CreatePrice(BaseModel):
    price: float
    currency_id: int
    width1: float
    width2: float
    height1: float
    height2: float
    collaction_id: int


class UpdatePrice(BaseModel):
    id: int
    price: float
    currency_id: int
    width1: float
    width2: float
    height1: float
    height2: float
    collaction_id: int