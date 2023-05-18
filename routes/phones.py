import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.phones import all_phones
from models.phones import Phones
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

phones_router = APIRouter(
    prefix="/phones",
    tags=["Phones operation"]
)


@phones_router.get("/get_phones")
def get_phones(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Phones, id)
    return all_phones(search, page, limit, db)
