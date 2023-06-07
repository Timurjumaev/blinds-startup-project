from models.categories import Categories
from utils.db_operations import save_in_db, get_in_db
from models.stages import Stages


def create_stage_e(form, db):
    get_in_db(db, Categories, form.category_id)
    new_stage_db = Stages(
        name=form.name,
        comment=form.comment,
        category_id=form.category_id,
        number=form.number
    )
    save_in_db(db, new_stage_db)


def update_stage_e(form, db):
    get_in_db(db, Stages, form.id), get_in_db(db, Categories, form.category_id)
    db.query(Stages).filter(Stages.id == form.id).update({
        Stages.name: form.name,
        Stages.comment: form.comment,
        Stages.category_id: form.category_id,
        Stages.number: form.number,
    })
    db.commit()