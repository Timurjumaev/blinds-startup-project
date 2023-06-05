import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.warehouse_materials import Warehouse_materials
from functions.warehouse_materials import all_warehouse_materials, update_warehouse_materials_s
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.users import CreateUser
from schemas.warehouse_materials import UpdateWarehouse_materials
from db import database
from utils.role_verification import role_verification

warehouse_materials_router = APIRouter(
    prefix="/warehouse_materials",
    tags=["Warehouse materials operation"]
)


@warehouse_materials_router.get("/get_warehouse_materials")
def get_warehouse_materials(search: str = None, id: int = 0, page: int = 0, limit: int = 25,
                            material_id: int = None, mechanism_id: int = None, db: Session = Depends(database),
                            current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Warehouse_materials, id)
    return all_warehouse_materials(search, page, limit, material_id, mechanism_id, db)


@warehouse_materials_router.put("/update_warehouse_materials")
def update_warehouse_materials(this_warehouse_material: UpdateWarehouse_materials, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_warehouse_materials_s(this_warehouse_material, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")