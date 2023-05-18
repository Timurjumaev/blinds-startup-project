from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.categories import create_category_y, update_category_y, all_categories
from models.categories import Categories
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.users import CreateUser
from schemas.categories import CreateCategory, UpdateCategory
from db import database

import inspect
from utils.role_verification import role_verification



categories_router = APIRouter(
    prefix="/categories",
    tags=["Categories operation"]
)


@categories_router.get("/get_categories")
def get_categories(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Categories, id)
    return all_categories(search, page, limit, db)


@categories_router.post("/create_category")
def create_category(new_category: CreateCategory, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_category_y(new_category, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@categories_router.put("/update_category")
def update_category(this_category: UpdateCategory, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_category_y(this_category, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






