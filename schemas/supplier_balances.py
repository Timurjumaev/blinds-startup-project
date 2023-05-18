from pydantic import BaseModel


class CreateSupplier_balances(BaseModel):
    balance: float
    currency_id: int


class UpdateSupplier_balances(BaseModel):
    id: int
    balance: float
    currency_id: int
