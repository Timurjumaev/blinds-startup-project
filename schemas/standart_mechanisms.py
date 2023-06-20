from pydantic import BaseModel


class CreateStandart_mechanism(BaseModel):
    mechanism_id: int
    quantity: int


class UpdateStandart_mechanism(BaseModel):
    id: int
    mechanism_id: int
    quantity: int
