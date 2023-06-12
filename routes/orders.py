import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.orders import all_orders, create_order_r, update_order_r, delete_order_r, one_order_r
from models.orders import Orders
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.orders import CreateOrder, UpdateOrder
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

orders_router = APIRouter(
    prefix="/orders",
    tags=["Orders operation"]
)


@orders_router.get("/get_orders")
def get_orders(search: str = None, id: int = 0, page: int = 0, limit: int = 25, customer_id: int = None,
               db: Session = Depends(database), current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return one_order_r(id, db)
    return all_orders(search, page, limit, customer_id, db)


@orders_router.post("/create_order")
def create_order(new_order: CreateOrder, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_order_r(new_order, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@orders_router.put("/update_order")
def update_order(this_order: UpdateOrder, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_order_r(this_order, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@orders_router.delete("/delete_order")
def delete_order(id: int, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_order_r(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






