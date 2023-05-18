from pydantic import BaseModel


class CreateStage_user(BaseModel):
    user_id: int
    kpi: float
    stage_id: int


class UpdateStage_user(BaseModel):
    id: int
    user_id: int
    kpi: float
    stage_id: int

