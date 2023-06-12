import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.expenses import all_expenses, create_expense_e, delete_expense_e
from models.expenses import Expenses
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.expenses import CreateExpense
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

expenses_router = APIRouter(
    prefix="/expenses",
    tags=["Expenses operation"]
)


@expenses_router.get("/get_expenses")
def get_expenses(search: str = None, id: int = 0, page: int = 0, limit: int = 25, kassa_id: int = None,
                 db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Expenses, id)
    return all_expenses(search, page, limit, kassa_id, db)


@expenses_router.post("/create_expense")
def create_expense(new_expense: CreateExpense, db: Session = Depends(database),
                   current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_expense_e(new_expense, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@expenses_router.delete("/delete_expense")
def delete_expense(id: int, db: Session = Depends(database),
                   current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_expense_e(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






