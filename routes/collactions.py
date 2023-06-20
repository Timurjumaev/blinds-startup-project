import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.collactions import create_collaction_n, update_collaction_n, all_collactions
from models.collactions import Collactions
from utils.login import get_current_active_user
from utils.db_operations import the_one
from schemas.users import CreateUser
from schemas.collactions import CreateCollaction, UpdateCollaction
from db import database
from utils.role_verification import role_verification

collactions_router = APIRouter(
    prefix="/collactions",
    tags=["Collactions operation"]
)


@collactions_router.get("/get_collactions")
def get_collactions(search: str = None, id: int = 0, page: int = 0, limit: int = 25, category_id: int = None,
                    db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return the_one(db, Collactions, id, current_user)
    return all_collactions(search, page, limit, category_id, db, current_user)


@collactions_router.post("/create_collaction")
def create_collaction(new_collaction: CreateCollaction, db: Session = Depends(database),
                      current_user: CreateUser = Depends(get_current_active_user)):
    if role_verification(current_user, inspect.currentframe().f_code.co_name):
        create_collaction_n(new_collaction, db, current_user)
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@collactions_router.put("/update_collaction")
def update_collaction(this_collaction: UpdateCollaction, db: Session = Depends(database),
                      current_user: CreateUser = Depends(get_current_active_user)):
    if role_verification(current_user, inspect.currentframe().f_code.co_name):
        update_collaction_n(this_collaction, db, current_user)
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")