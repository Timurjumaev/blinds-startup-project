from datetime import datetime
from sqlalchemy.orm import joinedload
from models.collactions import Collactions
from models.uploaded_files import Uploaded_files
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.mechanisms import Mechanisms
from fastapi import HTTPException


def all_mechanisms(search, page, limit, db):
    mechanisms = db.query(Mechanisms).options(joinedload(Mechanisms.collaction))
    if search:
        search_formatted = "%{}%".format(search)
        mechanisms = mechanisms.filter(Mechanisms.name.like(search_formatted) | Collactions.name.like(search_formatted))
    mechanisms = mechanisms.order_by(Mechanisms.name.asc())
    return pagination(mechanisms, page, limit)


def create_mechanism_m(form, db):
    get_in_db(db, Collactions, form.collaction_id)
    if form.file is None:
        raise HTTPException(status_code=400, detail="File is none!")
    new_mechanism_db = Mechanisms(
        name=form.name,
        comment=form.comment,
        collaction_id=form.collaction_id,
        olchov=form.olchov
    )
    save_in_db(db, new_mechanism_db)
    new_file_db = Uploaded_files(
        file=form.file,
        source="material",
        source_id=new_mechanism_db.id,
        time=datetime.now()
    )
    save_in_db(db, new_file_db)


def update_mechanism_m(form, db):
    get_in_db(db, Mechanisms, form.id), get_in_db(db, Collactions, form.collaction_id)
    db.query(Mechanisms).filter(Mechanisms.id == form.id).update({
        Mechanisms.name: form.name,
        Mechanisms.comment: form.comment,
        Mechanisms.collaction_id: form.collaction_id,
        Mechanisms.olchov: form.olchov,
    })
    db.commit()
    if form.file:
        db.query(Uploaded_files).filter(Uploaded_files.source == "mechanism",
                                        Uploaded_files.source_id == form.id).delete()
        db.commit()
        new_file_db = Uploaded_files(
            file=form.file,
            source="mechanism",
            source_id=form.id,
            time=datetime.now()
        )
        save_in_db(db, new_file_db)
