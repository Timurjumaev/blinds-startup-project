import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.stages import create_stage_e, update_stage_e, all_stages
from models.stages import Stages
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.users import CreateUser
from schemas.stages import CreateStage, UpdateStage
from db import database
from utils.role_verification import role_verification

stages_router = APIRouter(
    prefix="/stages",
    tags=["Stages operation"]
)


@stages_router.get("/get_stages")
def get_stages(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Stages, id)
    return all_stages(search, page, limit, db)


@stages_router.post("/create_stage")
def create_stage(new_stage: CreateStage, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_stage_e(new_stage, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@stages_router.put("/update_stage")
def update_stage(this_stage: UpdateStage, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_stage_e(this_stage, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")