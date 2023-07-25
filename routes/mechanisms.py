import inspect
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload
from functions.mechanisms import create_mechanism_m, update_mechanism_m, all_mechanisms
from models.mechanisms import Mechanisms
from utils.login import get_current_active_user
from schemas.users import CreateUser
from schemas.mechanisms import UpdateMechanism
from db import database
from utils.role_verification import role_verification

mechanisms_router = APIRouter(
    prefix="/mechanisms",
    tags=["Mechanisms operation"]
)


@mechanisms_router.get("/get_mechanisms")
def get_mechanisms(search: str = None, id: int = 0, page: int = 0, limit: int = 25, collaction_id: int = None,
                   db: Session = Depends(database), current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return db.query(Mechanisms).filter(Mechanisms.branch_id == current_user.branch_id,
                                           Mechanisms.id == id).options(joinedload(Mechanisms.files)).first()
    return all_mechanisms(search, page, limit, collaction_id, db, current_user)


@mechanisms_router.post("/create_mechanism")
def create_mechanism(name: str = Form(...), comment: str = Form(...), collaction_id: int = Form(...),
                     olchov: str = Form(...),
                     db: Session = Depends(database),
                     current_user: CreateUser = Depends(get_current_active_user),
                     file: UploadFile = File(None)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_mechanism_m(name, comment, collaction_id, olchov, db, current_user, file)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@mechanisms_router.put("/update_mechanism")
def update_mechanism(this_mechanism: UpdateMechanism, db: Session = Depends(database),
                     current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_mechanism_m(this_mechanism, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")