import os
from fastapi import HTTPException, UploadFile, File
from sqlalchemy.orm import joinedload
from models.categories import Categories
from models.uploaded_files import Uploaded_files
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.collactions import Collactions


def all_collactions(search, page, limit, cat_id, db, thisuser):
    collactions = db.query(Collactions).filter(Collactions.branch_id == thisuser.branch_id).\
        options(joinedload(Collactions.files))
    if search:
        search_formatted = "%{}%".format(search)
        collactions = collactions.filter(Collactions.name.like(search_formatted))
    if cat_id:
        collactions = collactions.filter(Collactions.category_id == cat_id)
    collactions = collactions.order_by(Collactions.name.asc())
    return pagination(collactions, page, limit)


def create_collaction_n(name, category_id, db, thisuser, file):
    the_one(db, Categories, category_id, thisuser)
    new_collaction_db = Collactions(
        name=name,
        category_id=category_id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_collaction_db)
    if file:
        file_location = file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpg", ".png", ".mp3", ".mp4", ".gif", ".jpeg"]:
            raise HTTPException(status_code=400, detail="Yuklanayotgan fayl formati mos kelmaydi!")
        with open(f"uploaded_files/{file_location}", "wb+") as file_object:
            file_object.write(file.file.read())
        new_file_db = Uploaded_files(
            file=file.filename,
            source="collaction",
            source_id=new_collaction_db.id,
            branch_id=thisuser.branch_id
        )
        save_in_db(db, new_file_db)


def update_collaction_n(form, db, user):
    the_one(db, Collactions, form.id, user), the_one(db, Categories, form.category_id, user)
    db.query(Collactions).filter(Collactions.id == form.id).update({
        Collactions.name: form.name,
        Collactions.category_id: form.category_id
    })
    db.commit()


