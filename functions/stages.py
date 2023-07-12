from models.categories import Categories
from utils.db_operations import save_in_db, the_one
from models.stages import Stages
from fastapi import HTTPException


def create_stage_e(form, db, thisuser):
    the_one(db, Categories, form.category_id, thisuser)
    if db.query(Stages).filter(Stages.number == form.number).first():
        raise HTTPException(status_code=400, detail="Bunday raqamli bosqich mavjud!")
    new_stage_db = Stages(
        name=form.name,
        comment=form.comment,
        category_id=form.category_id,
        number=form.number,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_stage_db)


def update_stage_e(form, db, user):
    the_one(db, Stages, form.id, user), the_one(db, Categories, form.category_id, user)
    this_stage = the_one(db, Stages, form.id, user)
    if db.query(Stages).filter(Stages.number == form.number).first() and form.number != this_stage.number:
        raise HTTPException(status_code=400, detail="Bunday raqamli bosqich mavjud!")
    db.query(Stages).filter(Stages.id == form.id).update({
        Stages.name: form.name,
        Stages.comment: form.comment,
        Stages.category_id: form.category_id,
        Stages.number: form.number,
    })
    db.commit()
