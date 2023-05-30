from pydantic import BaseModel


class CreateSupply(BaseModel):
    material_id: int
    width: float
    height: float
    mechanism_id: int
    quantity: float
    price: float
    currency_id: int
    supplier_id: int


class UpdateSupply(BaseModel):
    id: int
    material_id: int
    width: float
    height: float
    mechanism_id: int
    quantity: float
    price: float
    currency_id: int
    supplier_id: int
    status: bool
    warehouse_id: int
    cell_id: int
