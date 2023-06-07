import os
from fastapi import HTTPException
from models.collactions import Collactions
from models.materials import Materials
from models.mechanisms import Mechanisms
from models.uploaded_files import Uploaded_files
from models.users import Users
from utils.db_operations import save_in_db, get_in_db


def create_file_e(new_file, source, source_id, db):
    if db.query(Uploaded_files).filter(Uploaded_files.source == source,
                                       Uploaded_files.source_id == source_id).first():
        raise HTTPException(status_code=400, detail="This source already have his own file!")
    if (db.query(Users).filter(Users.id == source_id).first() and source == "user") or \
       (db.query(Users).filter(Collactions.id == source_id).first() and source == "collaction") or \
       (db.query(Users).filter(Materials.id == source_id).first() and source == "material") or \
       (db.query(Users).filter(Mechanisms.id == source_id).first() and source == "mechanism"):
        file_location = new_file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpg", ".png", ".mp3", ".mp4", ".gif", ".jpeg"]:
            raise HTTPException(status_code=400, detail="Yuklanayotgan fayl formati mos kelmaydi!")
        with open(f"uploaded_files/{file_location}", "wb+") as file_object:
            file_object.write(new_file.file.read())
        new_file_db = Uploaded_files(
            file=new_file.filename,
            source=source,
            source_id=source_id,
        )
        save_in_db(db, new_file_db)
    else:
        raise HTTPException(status_code=400, detail="Source error!")


def update_file_e(id, new_file, source, source_id, db):
    get_in_db(db, Uploaded_files, id)
    this_file = db.query(Uploaded_files).filter(Uploaded_files.source == source,
                                                Uploaded_files.source_id == source_id).first()
    if this_file and this_file.id != id:
        raise HTTPException(status_code=400,
                            detail="Siz kiritayotgan idli file ushbu sourcega tegishli "
                                   "emas va siz kiritayotgan sourcening ozini fayli bor")
    if (db.query(Users).filter(Users.id == source_id).first() and source == "user") or \
       (db.query(Users).filter(Collactions.id == source_id).first() and source == "collaction") or \
       (db.query(Users).filter(Materials.id == source_id).first() and source == "material") or \
       (db.query(Users).filter(Mechanisms.id == source_id).first() and source == "mechanism"):
        file_location = new_file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpg", ".png", ".mp3", ".mp4", ".gif", ".jpeg"]:
            raise HTTPException(status_code=400, detail="Yuklanayotgan fayl formati mos kelmaydi!")
        with open(f"uploaded_files/{file_location}", "wb+") as file_object:
            file_object.write(new_file.file.read())
        db.query(Uploaded_files).filter(Uploaded_files.id == id).update({
            Uploaded_files.file: new_file.filename,
            Uploaded_files.source: source,
            Uploaded_files.source_id: source_id,
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Source error!")


def delete_file_e(id, db):
    get_in_db(db, Uploaded_files, id)
    db.query(Uploaded_files).filter(Uploaded_files.id == id).delete()
    db.commit()



