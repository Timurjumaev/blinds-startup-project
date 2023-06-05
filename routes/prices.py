import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.prices import all_prices, create_price_e, update_price_e
from models.prices import Prices
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.users import CreateUser
from schemas.prices import CreatePrice, UpdatePrice
from db import database
from utils.role_verification import role_verification

prices_router = APIRouter(
    prefix="/prices",
    tags=["Prices operation"]
)


@prices_router.get("/get_prices")
def get_prices(id: int = 0, page: int = 0, limit: int = 25, collaction_id: int = None, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Prices, id)
    return all_prices(page, limit, collaction_id, db)


@prices_router.post("/create_price")
def create_price(new_price: CreatePrice, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_price_e(new_price, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@prices_router.put("/update_price")
def update_category(this_price: UpdatePrice, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_price_e(this_price, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")