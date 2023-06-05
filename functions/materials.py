from datetime import datetime

from models.collactions import Collactions
from models.uploaded_files import Uploaded_files
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.materials import Materials
from fastapi import HTTPException


def all_materials(search, page, limit, col_id, db):
    materials = db.query(Materials)
    if search:
        search_formatted = "%{}%".format(search)
        materials = materials.filter(Materials.name.like(search_formatted))
    if col_id:
        materials = materials.filter(Materials.collaction_id == col_id)
    materials = materials.order_by(Materials.name.asc())
    return pagination(materials, page, limit)


def create_material_l(form, db):
    get_in_db(db, Collactions, form.collaction_id)
    if form.file is None:
        raise HTTPException(status_code=400, detail="File is none!")
    new_material_db = Materials(
        name=form.name,
        comment=form.comment,
        collaction_id=form.collaction_id
    )
    save_in_db(db, new_material_db)
    new_file_db = Uploaded_files(
        file=form.file,
        source="material",
        source_id=new_material_db.id,
        time=datetime.now()
    )
    save_in_db(db, new_file_db)


def update_material_l(form, db):
    get_in_db(db, Materials, form.id), get_in_db(db, Collactions, form.collaction_id)
    db.query(Materials).filter(Materials.id == form.id).update({
        Materials.name: form.name,
        Materials.comment: form.comment,
        Materials.collaction_id: form.collaction_id
    })
    db.commit()
    if form.file:
        db.query(Uploaded_files).filter(Uploaded_files.source == "material",
                                        Uploaded_files.source_id == form.id).delete()
        db.commit()
        new_file_db = Uploaded_files(
            file=form.file,
            source="material",
            source_id=form.id,
            time=datetime.now()
        )
        save_in_db(db, new_file_db)


