from pydantic import BaseModel


class CreateTrade(BaseModel):
    material_id: int
    width: float
    height: float
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


class RequestMaterial(BaseModel):
    material_id: int
    width: float
    height: float


class CreateMaterial(BaseModel):
    warehouse_materials_id: int
    material_id: int
    width: float
    height: float


class UpdateMaterial(BaseModel):
    trade_id: int
    warehouse_materials_id: int
    material_id: int
    width: float
    height: float


class NextStage(BaseModel):
    id: int

