import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.incomes import all_incomes, create_income_e, update_income_e, delete_income_e
from models.incomes import Incomes
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.incomes import CreateIncome, UpdateIncome
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

incomes_router = APIRouter(
    prefix="/incomes",
    tags=["Incomes operation"]
)


@incomes_router.get("/get_incomes")
def get_incomes(search: str = None, id: int = 0, page: int = 0, limit: int = 25, kassa_id: int = None,
                db: Session = Depends(database), current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Incomes, id)
    return all_incomes(search, page, limit, kassa_id, db)


@incomes_router.post("/create_income")
def create_income(new_income: CreateIncome, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_income_e(new_income, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@incomes_router.put("/update_income")
def update_income(this_income: UpdateIncome, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_income_e(this_income, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@incomes_router.delete("/delete_income")
def delete_income(id: int, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_income_e(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






