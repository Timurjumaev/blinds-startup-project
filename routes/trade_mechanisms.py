import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.trade_mechanisms import create_trade_mechanism_m, all_trade_mechanisms, update_trade_mechanism_m, \
    delete_trade_mechanism_m
from models.trade_mechanisms import Trade_mechanisms
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.trade_mechanisms import CreateTrade_mechanism, UpdateTrade_mechanism
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

trade_mechanisms_router = APIRouter(
    prefix="/trade_mechanisms",
    tags=["Trade_mechanisms operation"]
)


@trade_mechanisms_router.get("/get_trade_mechanisms")
def get_trade_mechanisms(search: str = None, id: int = 0, page: int = 0, limit: int = 25, trade_id: int = None,
                         db: Session = Depends(database), current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Trade_mechanisms, id)
    return all_trade_mechanisms(search, page, limit, trade_id, db)


@trade_mechanisms_router.post("/create_trade_mechanism")
def create_trade_mechanism(new_trade_mechanism: CreateTrade_mechanism, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_trade_mechanism_m(new_trade_mechanism, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@trade_mechanisms_router.put("/update_trade_mechanism")
def update_trade_mechanism(this_trade_mechanism: UpdateTrade_mechanism, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_trade_mechanism_m(this_trade_mechanism, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@trade_mechanisms_router.delete("/delete_trade_mechanism")
def delete_trade_mechanism(id: int, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_trade_mechanism_m(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
