import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.cells import create_cell_l, update_cell_l, all_cells
from models.cells import Cells
from utils.login import get_current_active_user
from schemas.users import CreateUser
from schemas.cells import CreateCell, UpdateCell
from db import database
from utils.role_verification import role_verification
from utils.db_operations import the_one

cells_router = APIRouter(
    prefix="/cells",
    tags=["Cells operation"]
)


@cells_router.get("/get_cells")
def get_cells(search: str = None, id: int = 0, page: int = 0, limit: int = 25,
              warehouse_id: int = None, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return the_one(db, Cells, id, current_user)
    return all_cells(search, page, limit, warehouse_id, db, current_user)


@cells_router.post("/create_stage")
def create_stage(new_cell: CreateCell, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_cell_l(new_cell, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@cells_router.put("/update_cell")
def update_cell(this_cell: UpdateCell, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_cell_l(this_cell, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")