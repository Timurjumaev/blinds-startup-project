import inspect
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload
from functions.materials import create_material_l, update_material_l, all_materials
from models.materials import Materials
from utils.login import get_current_active_user
from schemas.users import CreateUser
from schemas.materials import UpdateMaterial
from db import database
from utils.role_verification import role_verification

materials_router = APIRouter(
    prefix="/materials",
    tags=["Materials operation"]
)


@materials_router.get("/get_materials")
def get_materials(search: str = None, id: int = 0, page: int = 0, limit: int = 25, collaction_id: int = None,
                  db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return db.query(Materials).filter(Materials.branch_id == current_user.branch_id,
                                          Materials.id == id).options(joinedload(Materials.files)).first()
    return all_materials(search, page, limit, collaction_id, db, current_user)


@materials_router.post("/create_material")
def create_material(name: str = Form(...), comment: str = Form(...), collaction_id: int = Form(...),
                    db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user), file: UploadFile = File(None)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_material_l(name, comment, collaction_id, db, current_user, file)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@materials_router.put("/update_material")
def update_material(this_material: UpdateMaterial, db: Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_material_l(this_material, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")