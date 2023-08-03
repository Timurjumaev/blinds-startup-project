import inspect
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.trades import all_trades, create_trade_e, update_trade_e, delete_trade_e, request_materials_s, \
    create_trade_material_s, update_trade_material_s, one_trade
from models.trades import Trades
from utils.login import get_current_active_user
from utils.db_operations import the_one
from schemas.trades import CreateTrade, UpdateTrade, RequestMaterial, CreateMaterial, UpdateMaterial, NextStage
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

trades_router = APIRouter(
    prefix="/trades",
    tags=["Trades operation"]
)


@trades_router.get("/get_trades")
def get_trades(search: str = None, id: int = 0, page: int = 0,
               limit: int = 25, order_id: int = None, stage_id: int = None, arxiv: bool = False,
               db: Session = Depends(database), current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return the_one(db, Trades, id, current_user)
    return all_trades(search, page, limit, order_id, stage_id, db, arxiv, current_user)


@trades_router.post("/create_trade")
async def create_trade(new_trade: CreateTrade, db: Session = Depends(database),
                       current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    await create_trade_e(new_trade, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@trades_router.put("/update_trade")
async def update_trade(this_trade: UpdateTrade, db: Session = Depends(database),
                       current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    await update_trade_e(this_trade, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@trades_router.delete("/delete_trade")
def delete_trade(id: int, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_trade_e(id, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@trades_router.post("/request_materials")
def request_materials(new_request_materials: RequestMaterial, db: Session = Depends(database),
                      current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return request_materials_s(new_request_materials, db, current_user)


@trades_router.post("/create_trade_material")
def create_trade_material(new_create_trade_material: CreateMaterial, db: Session = Depends(database),
                          current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return create_trade_material_s(new_create_trade_material, db, current_user)


@trades_router.post("/update_trade_material")
def update_trade_material(this_update_trade_material: UpdateMaterial, db: Session = Depends(database),
                          current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return update_trade_material_s(this_update_trade_material, db, current_user)


@trades_router.put("/next_stage")
def next_stage(form: List[NextStage], db: Session = Depends(database),
               current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return one_trade(form, db, current_user)






