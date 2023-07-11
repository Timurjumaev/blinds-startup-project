import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.branches import all_branches, create_branch_ch, update_branch_ch, one_branch
from models.branches import Branches
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.branches import CreateBranch, UpdateBranch
from schemas.users import CreateUser
from db import database
from utils.role_verification import role_verification

branches_router = APIRouter(
    prefix="/branches",
    tags=["Branches operation"]
)


@branches_router.get("/get_branches")
def get_branches(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return one_branch(db, id)
    return all_branches(search, page, limit, db)


@branches_router.post("/create_branch")
def create_branch(new_branch: CreateBranch, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_branch_ch(new_branch, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@branches_router.put("/update_branch")
def update_branch(this_branch: UpdateBranch, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_branch_ch(this_branch, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






