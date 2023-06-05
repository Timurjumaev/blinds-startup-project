from pydantic import BaseModel


class CreateMaterial(BaseModel):
    name: str
    comment: str
    collaction_id: int
    file: str



class UpdateMaterial(BaseModel):
    id: int
    name: str
    comment: str
    collaction_id: int
    file: str
