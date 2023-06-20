import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.standart_mechanisms import all_standart_mechanisms, create_standart_mechanism_m, \
    update_standart_mechanism_m, delete_standart_mechanism_m
from models.standart_mechanisms import Standart_mechanisms
from utils.login import get_current_active_user
from utils.db_operations import the_one
from schemas.standart_mechanisms import CreateStandart_mechanism, UpdateStandart_mechanism
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

standart_mechanisms_router = APIRouter(
    prefix="/standart_mechanisms",
    tags=["Standart_mechanisms operation"]
)


@standart_mechanisms_router.get("/get_standart_mechanisms")
def get_standart_mechanisms(search: str = None, id: int = 0, page: int = 0, limit: int = 25, mechanism_id: int = None, db: Session = Depends(database),
                            current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return the_one(db, Standart_mechanisms, id, current_user)
    return all_standart_mechanisms(search, page, limit, mechanism_id, db, current_user)


@standart_mechanisms_router.post("/create_standart_mechanism")
def create_standart_mechanism(new_standart_mechanism: CreateStandart_mechanism, db: Session = Depends(database),
                              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_standart_mechanism_m(new_standart_mechanism, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@standart_mechanisms_router.put("/update_standart_mechanism")
def update_standart_mechanism(this_standart_mechanism: UpdateStandart_mechanism, db: Session = Depends(database),
                              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_standart_mechanism_m(this_standart_mechanism, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@standart_mechanisms_router.delete("/delete_standart_mechanism")
def delete_standart_mechanism(id: int, db: Session = Depends(database),
                              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_standart_mechanism_m(id, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






