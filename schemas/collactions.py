from pydantic import BaseModel


class CreateCollaction(BaseModel):
    name: str
    category_id: int


class UpdateCollaction(BaseModel):
    id: int
    name: str
    category_id: int
