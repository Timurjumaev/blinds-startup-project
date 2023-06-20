from sqlalchemy.orm import joinedload
from models.collactions import Collactions
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.mechanisms import Mechanisms


def all_mechanisms(search, page, limit, db, thisuser):
    mechanisms = db.query(Mechanisms).filter(Mechanisms.branch_id == thisuser.branch_id)\
        .options(joinedload(Mechanisms.collaction),
                 joinedload(Mechanisms.files))
    if search:
        search_formatted = "%{}%".format(search)
        mechanisms = mechanisms.filter(Mechanisms.name.like(search_formatted) | Collactions.name.like(search_formatted))
    mechanisms = mechanisms.order_by(Mechanisms.name.asc())
    return pagination(mechanisms, page, limit)


def create_mechanism_m(form, db, thisuser):
    the_one(db, Collactions, form.collaction_id, thisuser)
    new_mechanism_db = Mechanisms(
        name=form.name,
        comment=form.comment,
        collaction_id=form.collaction_id,
        olchov=form.olchov,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_mechanism_db)


def update_mechanism_m(form, db, user):
    the_one(db, Mechanisms, form.id, user), the_one(db, Collactions, form.collaction_id, user)
    db.query(Mechanisms).filter(Mechanisms.id == form.id).update({
        Mechanisms.name: form.name,
        Mechanisms.comment: form.comment,
        Mechanisms.collaction_id: form.collaction_id,
        Mechanisms.olchov: form.olchov,
    })
    db.commit()

