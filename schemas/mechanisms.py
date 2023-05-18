from pydantic import BaseModel


class CreateMechanism(BaseModel):
    name: str
    comment: str
    collaction_id: int
    olchov: str


class UpdateMechanism(BaseModel):
    id: int
    name: str
    comment: str
    collaction_id: int
    olchov: str

