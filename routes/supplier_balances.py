import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.supplier_balances import all_supplier_balances
from models.supplier_balances import Supplier_balances
from utils.login import get_current_active_user
from utils.db_operations import the_one
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

supplier_balances_router = APIRouter(
    prefix="/supplier_balances",
    tags=["Supplier balances operation"]
)


@supplier_balances_router.get("/get_supplier_balances")
def get_supplier_balances(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
                          current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return the_one(db, Supplier_balances, id, current_user)
    return all_supplier_balances(search, page, limit, db, current_user)
