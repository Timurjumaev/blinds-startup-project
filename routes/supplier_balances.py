import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.supplier_balances import Supplier_balances
from utils.login import get_current_active_user
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

supplier_balances_router = APIRouter(
    prefix="/supplier_balances",
    tags=["Supplier balances operation"]
)


@supplier_balances_router.get("/get_supplier_balances")
def get_supplier_balances(supplier_id: int = 0, db: Session = Depends(database),
                          current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    balance = db.query(Supplier_balances).filter(Supplier_balances.branch_id == current_user.branch_id)
    if supplier_id:
        balance = balance.filter(Supplier_balances.supplier_id == supplier_id)
    return balance.all()
