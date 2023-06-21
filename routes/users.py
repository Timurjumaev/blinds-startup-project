import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.users import create_user_r, all_users, update_user_r
from models.users import Users
from utils.db_operations import the_one
from utils.login import get_current_active_user
from schemas.users import CreateUser, UpdateUser
from db import database
from utils.role_verification import role_verification

users_router = APIRouter(
    prefix="/users",
    tags=["Users operation"]
)


@users_router.get("/get_users")
def get_users(search: str = None, id: int = 0, page: int = 0, limit: int = 25, status: bool = None,
              db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return the_one(db, Users, id, current_user)
    return all_users(search, page, limit, status, db, current_user)


@users_router.post("/create_user")
def create_user(new_user: CreateUser, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_user_r(new_user, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@users_router.put("/update_user")
def update_user(this_user: UpdateUser, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_user_r(this_user, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@users_router.get("/request_user")
def request_user(current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return current_user






