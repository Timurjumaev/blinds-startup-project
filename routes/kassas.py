import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.kassas import all_kassas, create_kassa_a, update_kassa_a
from models.kassas import Kassas
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.kassas import CreateKassa, UpdateKassa
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

kassas_router = APIRouter(
    prefix="/kassas",
    tags=["Kassas operation"]
)


@kassas_router.get("/get_kassas")
def get_kassas(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Kassas, id)
    return all_kassas(search, page, limit, db)


@kassas_router.post("/create_kassa")
def create_kassa(new_kassa: CreateKassa, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_kassa_a(new_kassa, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@kassas_router.put("/update_kassa")
def update_kassa(this_kassa: UpdateKassa, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_kassa_a(this_kassa, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")









