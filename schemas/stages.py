from pydantic import BaseModel


class CreateStage(BaseModel):
    name: str
    comment: str
    category_id: int
    number: int


class UpdateStage(BaseModel):
    id: int
    name: str
    comment: str
    category_id: int
    number: int

    