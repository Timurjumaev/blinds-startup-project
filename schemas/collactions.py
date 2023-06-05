from pydantic import BaseModel


class CreateCollaction(BaseModel):
    name: str
    category_id: int
    file: str


class UpdateCollaction(BaseModel):
    id: int
    name: str
    category_id: int
    file: str
