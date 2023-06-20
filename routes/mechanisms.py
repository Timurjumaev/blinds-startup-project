import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.mechanisms import create_mechanism_m, update_mechanism_m, all_mechanisms
from models.mechanisms import Mechanisms
from utils.login import get_current_active_user
from utils.db_operations import the_one
from schemas.users import CreateUser
from schemas.mechanisms import CreateMechanism, UpdateMechanism
from db import database
from utils.role_verification import role_verification

mechanisms_router = APIRouter(
    prefix="/mechanisms",
    tags=["Mechanisms operation"]
)


@mechanisms_router.get("/get_mechanisms")
def get_mechanisms(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
                   current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return the_one(db, Mechanisms, id, current_user)
    return all_mechanisms(search, page, limit, db, current_user)


@mechanisms_router.post("/create_mechanism")
def create_mechanism(new_mechanism: CreateMechanism, db: Session = Depends(database),
                     current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_mechanism_m(new_mechanism, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@mechanisms_router.put("/update_mechanism")
def update_mechanism(this_mechanism: UpdateMechanism, db: Session = Depends(database),
                     current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_mechanism_m(this_mechanism, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")