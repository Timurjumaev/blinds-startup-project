from pydantic import BaseModel


class UpdateWarehouse_materials(BaseModel):
    id: int
    cell_id: int

