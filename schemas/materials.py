from pydantic import BaseModel


class CreateMaterial(BaseModel):
    name: str
    comment: str
    collaction_id: int


class UpdateMaterial(BaseModel):
    id: int
    name: str
    comment: str
    collaction_id: int