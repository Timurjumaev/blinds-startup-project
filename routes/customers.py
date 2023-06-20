import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.customers import all_customers, create_customer_r, update_customer_r
from models.customers import Customers
from utils.login import get_current_active_user
from utils.db_operations import the_one
from schemas.customers import CreateCustomer, UpdateCustomer
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

customers_router = APIRouter(
    prefix="/customers",
    tags=["Customers operation"]
)


@customers_router.get("/get_customers")
def get_customers(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return the_one(db, Customers, id, current_user)
    return all_customers(search, page, limit, db, current_user)


@customers_router.post("/create_customer")
def create_customer(new_customer: CreateCustomer, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_customer_r(new_customer, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@customers_router.put("/update_customer")
def update_customer(this_customer: UpdateCustomer, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_customer_r(this_customer, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






