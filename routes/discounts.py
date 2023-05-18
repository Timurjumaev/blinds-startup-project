import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.discounts import all_discounts, create_discount_t, update_discount_t, delete_discount_t
from models.discounts import Discounts
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.discounts import CreateDiscount, UpdateDiscount
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

discounts_router = APIRouter(
    prefix="/discounts",
    tags=["Discounts operation"]
)


@discounts_router.get("/get_discounts")
def get_discounts(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Discounts, id)
    return all_discounts(search, page, limit, db)


@discounts_router.post("/create_discount")
def create_discount(new_discount: CreateDiscount, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_discount_t(new_discount, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@discounts_router.put("/update_discount")
def update_discount(this_discount: UpdateDiscount, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_discount_t(this_discount, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@discounts_router.delete("/delete_discount")
def delete_discount(id: int, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_discount_t(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






