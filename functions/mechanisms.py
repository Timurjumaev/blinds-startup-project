import os
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.collactions import Collactions
from models.uploaded_files import Uploaded_files
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.mechanisms import Mechanisms


def all_mechanisms(search, page, limit, collaction_id, db, thisuser):
    mechanisms = db.query(Mechanisms).filter(Mechanisms.branch_id == thisuser.branch_id)\
        .options(joinedload(Mechanisms.collaction),
                 joinedload(Mechanisms.files),
                 joinedload(Mechanisms.standart_mechanism))
    if collaction_id:
        collaction_filter = Mechanisms.collaction_id == collaction_id
    else:
        collaction_filter = Mechanisms.id > 0
    if search:
        search_formatted = "%{}%".format(search)
        mechanisms = mechanisms.filter(Mechanisms.name.like(search_formatted) | Collactions.name.like(search_formatted))
    mechanisms = mechanisms.filter(collaction_filter).order_by(Mechanisms.name.asc())
    return pagination(mechanisms, page, limit)


def create_mechanism_m(name, comment, collaction_id, olchov, db, thisuser, file):
    the_one(db, Collactions, collaction_id, thisuser)
    new_mechanism_db = Mechanisms(
        name=name,
        comment=comment,
        collaction_id=collaction_id,
        olchov=olchov,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_mechanism_db)
    if file:
        file_location = file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpg", ".png", ".mp3", ".mp4", ".gif", ".jpeg"]:
            raise HTTPException(status_code=400, detail="Yuklanayotgan fayl formati mos kelmaydi!")
        with open(f"uploaded_files/{file_location}", "wb+") as file_object:
            file_object.write(file.file.read())
        new_file_db = Uploaded_files(
            file=file.filename,
            source="mechanism",
            source_id=new_mechanism_db.id,
            branch_id=thisuser.branch_id
        )
        save_in_db(db, new_file_db)


def update_mechanism_m(form, db, user):
    the_one(db, Mechanisms, form.id, user), the_one(db, Collactions, form.collaction_id, user)
    db.query(Mechanisms).filter(Mechanisms.id == form.id).update({
        Mechanisms.name: form.name,
        Mechanisms.comment: form.comment,
        Mechanisms.collaction_id: form.collaction_id,
        Mechanisms.olchov: form.olchov,
    })
    db.commit()

