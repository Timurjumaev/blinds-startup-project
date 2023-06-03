from typing import List

from pydantic import BaseModel
from models.standart_mechanisms import Standart_mechanisms

mechanisms = []
widths = []
quantities = []
for mechanism, width, quantity in Standart_mechanisms.mechanism_id, Standart_mechanisms.width, Standart_mechanisms.quantity:
    mechanisms.append(mechanism)
    widths.append(width)
    quantities.append(quantity)


class CreateTrade_mechanism(BaseModel):
    trade_id: int
    mechanism_id: int
    width: float
    quantity: int


class UpdateTrade_mechanism(BaseModel):
    id: int
    trade_id: int
    mechanism_id: int
    width: float
    quantity: int

