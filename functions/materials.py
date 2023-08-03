import os
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.collactions import Collactions
from models.uploaded_files import Uploaded_files
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.materials import Materials


def all_materials(search, page, limit, col_id, db, thisuser):
    materials = db.query(Materials).filter(Materials.branch_id == thisuser.branch_id)\
        .options(joinedload(Materials.files),
                 joinedload(Materials.collaction).options(joinedload(Collactions.category)))
    if search:
        search_formatted = "%{}%".format(search)
        materials = materials.filter(Materials.name.like(search_formatted))
    if col_id:
        materials = materials.filter(Materials.collaction_id == col_id)
    materials = materials.order_by(Materials.name.asc())
    return pagination(materials, page, limit)


def create_material_l(name, comment, collaction_id, db, thisuser, file):
    the_one(db, Collactions, collaction_id, thisuser)
    new_material_db = Materials(
        name=name,
        comment=comment,
        collaction_id=collaction_id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_material_db)
    if file:
        file_location = file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpg", ".png", ".mp3", ".mp4", ".gif", ".jpeg"]:
            raise HTTPException(status_code=400, detail="Yuklanayotgan fayl formati mos kelmaydi!")
        with open(f"uploaded_files/{file_location}", "wb+") as file_object:
            file_object.write(file.file.read())
        new_file_db = Uploaded_files(
            file=file.filename,
            source="material",
            source_id=new_material_db.id,
            branch_id=thisuser.branch_id
        )
        save_in_db(db, new_file_db)


def update_material_l(form, db, user):
    the_one(db, Materials, form.id, user), the_one(db, Collactions, form.collaction_id, user)
    db.query(Materials).filter(Materials.id == form.id).update({
        Materials.name: form.name,
        Materials.comment: form.comment,
        Materials.collaction_id: form.collaction_id
    })
    db.commit()



