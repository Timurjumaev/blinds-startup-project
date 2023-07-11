import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.incomes import all_incomes, create_income_e, delete_income_e
from models.incomes import Incomes
from utils.login import get_current_active_user
from utils.db_operations import the_one
from schemas.incomes import CreateIncome
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
        return the_one(db, Incomes, id, current_user)
    return all_incomes(search, page, limit, kassa_id, db, current_user)


@incomes_router.post("/create_income")
async def create_income(new_income: CreateIncome, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    await create_income_e(new_income, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@incomes_router.delete("/delete_income")
def delete_income(id: int, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_income_e(id, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






