import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.trades import all_trades, create_trade_e, update_trade_e, delete_trade_e
from models.trades import Trades
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.trades import CreateTrade, UpdateTrade
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

trades_router = APIRouter(
    prefix="/trades",
    tags=["Trades operation"]
)


@trades_router.get("/get_trades")
def get_trades(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Trades, id)
    return all_trades(search, page, limit, db)


@trades_router.post("/create_trade")
def create_trade(new_trade: CreateTrade, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_trade_e(new_trade, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@trades_router.put("/update_trade")
def update_trade(this_trade: UpdateTrade, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_trade_e(this_trade, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@trades_router.delete("/delete_trade")
def delete_trade(id: int, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_trade_e(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






