from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from functions.uploaded_files import create_file_e, update_file_e, delete_file_e
from utils.login import get_current_active_user
from schemas.users import CreateUser
from db import database
import inspect
from utils.role_verification import role_verification


files_router = APIRouter(
    prefix="/files",
    tags=["Files operation"]
)


@files_router.post("/create_file")
def create_file(source: str = Form(...), source_id: int = Form(...), new_file: UploadFile = File(...),
                db: Session = Depends(database), current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_file_e(new_file, source, source_id, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@files_router.put("/update_file")
def update_category(id: int = Form(...), source: str = Form(...),
                    source_id: int = Form(...), new_file: UploadFile = File(...),
                    db: Session = Depends(database), current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_file_e(id, new_file, source, source_id, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@files_router.delete("/delete_file")
def delete_file(id: int, db: Session = Depends(database), current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_file_e(id, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")








