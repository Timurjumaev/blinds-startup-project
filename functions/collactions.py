from datetime import datetime

from models.categories import Categories
from models.uploaded_files import Uploaded_files
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.collactions import Collactions
from fastapi import HTTPException


def all_collactions(search, page, limit, cat_id, db):
    collactions = db.query(Collactions)
    if search:
        search_formatted = "%{}%".format(search)
        collactions = collactions.filter(Collactions.name.like(search_formatted))
    if cat_id:
        collactions = collactions.filter(Collactions.category_id == cat_id)
    collactions = collactions.order_by(Collactions.name.asc())
    return pagination(collactions, page, limit)


def create_collaction_n(form, db):
    get_in_db(db, Categories, form.category_id)
    if form.file is None:
        raise HTTPException(status_code=400, detail="File is none!")
    new_collaction_db = Collactions(
        name=form.name,
        category_id=form.category_id
    )
    save_in_db(db, new_collaction_db)
    new_file_db = Uploaded_files(
        file=form.file,
        source="collaction",
        source_id=new_collaction_db.id,
        time=datetime.now()
    )
    save_in_db(db, new_file_db)


def update_collaction_n(form, db):
    get_in_db(db, Collactions, form.id), get_in_db(db, Categories, form.category_id)
    db.query(Collactions).filter(Collactions.id == form.id).update({
        Collactions.name: form.name,
        Collactions.category_id: form.category_id
    })
    db.commit()
    if form.file:
        db.query(Uploaded_files).filter(Uploaded_files.source == "collaction",
                                        Uploaded_files.source_id == form.id).delete()
        db.commit()
        new_file_db = Uploaded_files(
            file=form.file,
            source="collaction",
            source_id=form.id,
            time=datetime.now()
        )
        save_in_db(db, new_file_db)

