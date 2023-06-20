from sqlalchemy.orm import joinedload
from models.categories import Categories
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


def create_collaction_n(form, db, thisuser):
    the_one(db, Categories, form.category_id, thisuser)
    new_collaction_db = Collactions(
        name=form.name,
        category_id=form.category_id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_collaction_db)


def update_collaction_n(form, db, user):
    the_one(db, Collactions, form.id, user), the_one(db, Categories, form.category_id, user)
    db.query(Collactions).filter(Collactions.id == form.id).update({
        Collactions.name: form.name,
        Collactions.category_id: form.category_id
    })
    db.commit()


