import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.stage_users import create_stage_users_s, update_stage_users_s, all_stage_users, delete_stage_user_r
from models.stage_users import Stage_users
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.users import CreateUser
from schemas.stage_users import CreateStage_user, UpdateStage_user
from db import database
from utils.role_verification import role_verification

stage_users_router = APIRouter(
    prefix="/stage_users",
    tags=["Stage users operation"]
)


@stage_users_router.get("/get_stage_users")
def get_stage_users(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Stage_users, id)
    return all_stage_users(search, page, limit, db)


@stage_users_router.post("/create_stage_user")
def create_stage_user(new_stage_user: CreateStage_user, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_stage_users_s(new_stage_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@stage_users_router.put("/update_stage_user")
def update_stage_user(this_stage_user: UpdateStage_user, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_stage_users_s(this_stage_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@stage_users_router.delete("/delete_stage_user")
def delete_stage_user(id: int, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_stage_user_r(id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
