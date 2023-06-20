import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.warehouses import all_warehouses, create_warehouse_e, update_warehouse_e
from models.warehouses import Warehouses
from utils.login import get_current_active_user
from utils.db_operations import the_one
from schemas.warehouses import CreateWarehouse, UpdateWarehouse
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

warehouses_router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses operation"]
)


@warehouses_router.get("/get_warehouses")
def get_warehouses(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
                   current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return the_one(db, Warehouses, id, current_user)
    return all_warehouses(search, page, limit, db, current_user)


@warehouses_router.post("/create_warehouse")
def create_warehouse(new_warehouse: CreateWarehouse, db: Session = Depends(database),
                     current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_warehouse_e(new_warehouse, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@warehouses_router.put("/update_warehouse")
def update_warehouse(this_warehouse: UpdateWarehouse, db: Session = Depends(database),
                     current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_warehouse_e(this_warehouse, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






