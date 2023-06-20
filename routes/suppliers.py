import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.suppliers import create_supplier_r, update_supplier_r, all_suppliers
from models.suppliers import Suppliers
from utils.login import get_current_active_user
from utils.db_operations import the_one
from schemas.suppliers import CreateSupplier, UpdateSupplier
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

suppliers_router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers operation"]
)


@suppliers_router.get("/get_suppliers")
def get_suppliers(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return the_one(db, Suppliers, id, current_user)
    return all_suppliers(search, page, limit, db, current_user)


@suppliers_router.post("/create_supplier")
def create_supplier(new_supplier: CreateSupplier, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_supplier_r(new_supplier, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@suppliers_router.put("/update_supplier")
def update_supplier(this_supplier: UpdateSupplier, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_supplier_r(this_supplier, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






