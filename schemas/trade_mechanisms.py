from pydantic import BaseModel


class CreateTrade_mechanism(BaseModel):
    trade_id: int
    mechanism_id: int
    quantity: int


class UpdateTrade_mechanism(BaseModel):
    id: int
    trade_id: int
    mechanism_id: int
    quantity: int

