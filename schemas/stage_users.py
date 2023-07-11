from pydantic import BaseModel


class CreateStage_user(BaseModel):
    user_id: int
    kpi: float
    currency_id: int
    stage_id: int


class UpdateStage_user(BaseModel):
    id: int
    user_id: int
    kpi: float
    currency_id: int
    stage_id: int

