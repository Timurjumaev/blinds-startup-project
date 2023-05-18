from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    width_norm: float
    height_norm: float
    width_max: float
    height_max: float


class UpdateCategory(BaseModel):
    id: int
    name: str
    width_norm: float
    height_norm: float
    width_max: float
    height_max: float
