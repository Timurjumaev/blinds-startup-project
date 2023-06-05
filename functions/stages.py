from sqlalchemy.orm import joinedload

from models.categories import Categories
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.stages import Stages


def all_stages(search, page, limit, db):
    stages = db.query(Stages).options(joinedload(Stages.category))
    search_formatted = "%{}%".format(search)
    search_filter = (Stages.name.like(search_formatted)) | (Categories.name.like(search_formatted))
    if search:
        stages = stages.filter(search_filter).order_by(Stages.id.asc())
    else:
        stages = stages.order_by(Stages.id.asc())
    return pagination(stages, page, limit)


def create_stage_e(form, db):
    if get_in_db(db, Categories, form.category_id):
        new_stage_db = Stages(
            name=form.name,
            comment=form.comment,
            category_id=form.category_id,
            number=form.number
        )
        save_in_db(db, new_stage_db)





def update_stage_e(form, db):
    if get_in_db(db, Stages, form.id) and get_in_db(db, Categories, form.category_id):
        db.query(Stages).filter(Stages.id == form.id).update({
            Stages.name: form.name,
            Stages.comment: form.comment,
            Stages.category_id: form.category_id,
            Stages.number: form.number,
        })
        db.commit()