from pydantic import BaseModel


class CreateTrade(BaseModel):
    material_id: int
    width: float
    height: float
    stage_id: int
    comment: str
    order_id: int


class UpdateTrade(BaseModel):
    id: int
    material_id: int
    width: float
    height: float
    stage_id: int
    status: str
    comment: str
    order_id: int
