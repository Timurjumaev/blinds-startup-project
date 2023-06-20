from models.categories import Categories
from utils.db_operations import save_in_db, the_one
from models.stages import Stages


def create_stage_e(form, db, thisuser):
    the_one(db, Categories, form.category_id, thisuser)
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
    db.query(Stages).filter(Stages.id == form.id).update({
        Stages.name: form.name,
        Stages.comment: form.comment,
        Stages.category_id: form.category_id,
        Stages.number: form.number,
    })
    db.commit()
