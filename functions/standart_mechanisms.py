from sqlalchemy.orm import joinedload
from models.mechanisms import Mechanisms
from models.users import Users
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.standart_mechanisms import Standart_mechanisms
from fastapi import HTTPException


def all_standart_mechanisms(search, page, limit, mechanism_id, db, thisuser):
    standart_mechanism = db.query(Standart_mechanisms).filter(Standart_mechanisms.branch_id == thisuser.branch_id).\
        options(joinedload(Standart_mechanisms.mechanism),
                joinedload(Standart_mechanisms.user))
    if search and mechanism_id:
        search_formatted = "%{}%".format(search)
        standart_mechanism = standart_mechanism.filter(Users.name.like(search_formatted) |
                                                       Users.username.like(search_formatted) |
                                                       Mechanisms.name.like(search_formatted))
        standart_mechanism = standart_mechanism.filter(Standart_mechanisms.mechanism_id == mechanism_id)\
            .order_by(Standart_mechanisms.id.asc())
    elif search is None and mechanism_id:
        standart_mechanism = standart_mechanism.filter(Standart_mechanisms.mechanism_id == mechanism_id)\
            .order_by(Standart_mechanisms.id.asc())
    elif mechanism_id is None and search:
        search_formatted = "%{}%".format(search)
        standart_mechanism = standart_mechanism.filter(Users.name.like(search_formatted) |
                                                       Users.username.like(search_formatted) |
                                                       Mechanisms.name.like(search_formatted))
        standart_mechanism = standart_mechanism.order_by(Standart_mechanisms.id.asc())
    else:
        standart_mechanism = standart_mechanism.order_by(Standart_mechanisms.id.asc())
    return pagination(standart_mechanism, page, limit)


def create_standart_mechanism_m(form, db, thisuser):
    the_one(db, Mechanisms, form.mechanism_id, thisuser)
    if db.query(Standart_mechanisms).filter(Standart_mechanisms.mechanism_id == form.mechanism_id).first():
        raise HTTPException(status_code=400, detail="This mechanism already have his own standart_mechanism!")
    new_standart_mechanism_db = Standart_mechanisms(
        mechanism_id=form.mechanism_id,
        quantity=form.quantity,
        user_id=thisuser.id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_standart_mechanism_db)


def update_standart_mechanism_m(form, db, thisuser):
    the_one(db, Standart_mechanisms, form.id, thisuser), the_one(db, Mechanisms, form.mechanism_id, thisuser)
    sm = db.query(Standart_mechanisms).filter(Standart_mechanisms.id == form.id).first()
    if sm.mechanism_id == form.mechanism_id or db.query(Standart_mechanisms).filter(Standart_mechanisms.mechanism_id ==
                                                                                    form.mechanism_id).first() is None:
        db.query(Standart_mechanisms).filter(Standart_mechanisms.id == form.id).update({
            Standart_mechanisms.mechanism_id: form.mechanism_id,
            Standart_mechanisms.quantity: form.quantity,
            Standart_mechanisms.user_id: thisuser.id
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="This mechanism already have his own standart_mechanism!")


def delete_standart_mechanism_m(id, db, user):
    the_one(db, Standart_mechanisms, id, user)
    db.query(Standart_mechanisms).filter(Standart_mechanisms.id == id).delete()
    db.commit()
