import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.supplies import create_supply_y, update_supply_y, all_supplies
from models.supplies import Supplies
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.users import CreateUser
from schemas.supplies import CreateSupply, UpdateSupply
from db import database
from utils.role_verification import role_verification

supplies_router = APIRouter(
    prefix="/supplies",
    tags=["Supplies operation"]
)


@supplies_router.get("/get_supplies")
def get_supplies(search: str = None, id: int = 0, page: int = 0, limit: int = 25,
                 supplier_id: int = None, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Supplies, id)
    return all_supplies(search, page, limit, supplier_id, db)


@supplies_router.post("/create_supply")
def create_supply(new_supply: CreateSupply, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_supply_y(new_supply, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@supplies_router.put("/update_supply")
def update_supply(this_supply: UpdateSupply, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_supply_y(this_supply, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")