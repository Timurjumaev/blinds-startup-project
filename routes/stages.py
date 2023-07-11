import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from functions.stages import create_stage_e, update_stage_e
from models.stages import Stages
from utils.login import get_current_active_user
from schemas.users import CreateUser
from schemas.stages import CreateStage, UpdateStage
from db import database
from utils.role_verification import role_verification

stages_router = APIRouter(
    prefix="/stages",
    tags=["Stages operation"]
)


@stages_router.get("/get_stages")
def get_stages(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return db.query(Stages).filter(Stages.branch_id == current_user.branch_id).options(joinedload(Stages.category))\
        .order_by(Stages.id).all()


@stages_router.post("/create_stage")
def create_stage(new_stage: CreateStage, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_stage_e(new_stage, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@stages_router.put("/update_stage")
def update_stage(this_stage: UpdateStage, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_stage_e(this_stage, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
