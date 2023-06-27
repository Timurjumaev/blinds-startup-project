from pydantic import BaseModel


class CreateKassa(BaseModel):
    name: str
    currency_id: int


class UpdateKassa(BaseModel):
    id: int
    name: str



