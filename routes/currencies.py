import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.currencies import update_currency_y, create_currency_y
from models.currencies import Currencies
from utils.login import get_current_active_user
from schemas.users import CreateUser
from schemas.currencies import CreateCurrency, UpdateCurrency
from db import database
from utils.role_verification import role_verification
from utils.db_operations import the_one

currencies_router = APIRouter(
    prefix="/currencies",
    tags=["Currencies operation"]
)


@currencies_router.get("/get_currencies")
def get_currencies(id: int = 0, db: Session = Depends(database),
                   current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id > 0:
        return the_one(db, Currencies, id, current_user)
    return db.query(Currencies).filter(Currencies.branch_id == current_user.branch_id).all()


@currencies_router.post("/create_currency")
def create_currency(new_currency: CreateCurrency, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_currency_y(new_currency, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@currencies_router.put("/update_currency")
def update_currency(this_currency: UpdateCurrency, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_currency_y(this_currency, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")