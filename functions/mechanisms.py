from sqlalchemy.orm import joinedload

from models.collactions import Collactions
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.mechanisms import Mechanisms


def all_mechanisms(search, page, limit, db):
    mechanisms = db.query(Mechanisms).join(Mechanisms.collaction).options(joinedload(Mechanisms.collaction))
    if search:
        search_formatted = "%{}%".format(search)
        mechanisms = mechanisms.filter(Mechanisms.name.like(search_formatted) | Collactions.name.like(search_formatted))
    mechanisms = mechanisms.order_by(Mechanisms.name.asc())
    return pagination(mechanisms, page, limit)


def create_mechanism_m(form, db):
    if get_in_db(db, Collactions, form.collaction_id):
        new_mechanism_db = Mechanisms(
            name=form.name,
            comment=form.comment,
            collaction_id=form.collaction_id,
            olchov=form.olchov
        )
        save_in_db(db, new_mechanism_db)





def update_mechanism_m(form, db):
    if get_in_db(db, Mechanisms, form.id) and get_in_db(db, Collactions, form.collaction_id):
        db.query(Mechanisms).filter(Mechanisms.id == form.id).update({
            Mechanisms.name: form.name,
            Mechanisms.comment: form.comment,
            Mechanisms.collaction_id: form.collaction_id,
            Mechanisms.olchov: form.olchov,
        })
        db.commit()