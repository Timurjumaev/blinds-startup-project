import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.discounts import create_discount_t, delete_discount_t
from models.discounts import Discounts
from utils.login import get_current_active_user
from schemas.discounts import CreateDiscount
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

discounts_router = APIRouter(
    prefix="/discounts",
    tags=["Discounts operation"]
)


@discounts_router.get("/get_discounts")
def get_discounts(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return db.query(Discounts).all()


@discounts_router.post("/create_discount")
def create_discount(new_discount: CreateDiscount, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_discount_t(new_discount, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@discounts_router.delete("/delete_discount")
def delete_discount(id: int, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_discount_t(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






