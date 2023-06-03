from sqlalchemy.orm import joinedload
from models.mechanisms import Mechanisms
from models.users import Users
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.standart_mechanisms import Standart_mechanisms
from fastapi import HTTPException



def all_standart_mechanisms(search, page, limit, db):
    standart_mechanism = db.query(Standart_mechanisms).options(joinedload(Standart_mechanisms.mechanism),
                                                               joinedload(Standart_mechanisms.user))
    if search:
        search_formatted = "%{}%".format(search)
        standart_mechanism = standart_mechanism.filter(Users.name.like(search_formatted) |
                                                       Users.username.like(search_formatted) |
                                                       Mechanisms.name.like(search_formatted))
    standart_mechanism = standart_mechanism.order_by(Standart_mechanisms.id.asc())
    return pagination(standart_mechanism, page, limit)


def create_standart_mechanism_m(form, db, thisuser):
    get_in_db(db, Mechanisms, form.mechanism_id)
    if db.query(Standart_mechanisms).filter(Standart_mechanisms.mechanism_id == form.mechanism_id).first():
        raise HTTPException(status_code=400, detail="This mechanism already have his own standart_mechanism!")
    new_standart_mechanism_db = Standart_mechanisms(
        mechanism_id=form.mechanism_id,
        width=form.width,
        quantity=form.quantity,
        user_id=thisuser.id
    )
    save_in_db(db, new_standart_mechanism_db)

def update_standart_mechanism_m(form, db, thisuser):
    get_in_db(db, Standart_mechanisms, form.id), get_in_db(db, Mechanisms, form.mechanism_id)
    sm = db.query(Standart_mechanisms).filter(Standart_mechanisms.id == form.id).first()
    if sm.mechanism_id == form.mechanism_id or db.query(Standart_mechanisms).filter(Standart_mechanisms.mechanism_id ==
                                                                                    form.mechanism_id).first() is None:
        db.query(Standart_mechanisms).filter(Standart_mechanisms.id == form.id).update({
            Standart_mechanisms.mechanism_id: form.mechanism_id,
            Standart_mechanisms.width: form.width,
            Standart_mechanisms.quantity: form.quantity,
            Standart_mechanisms.user_id: thisuser.id
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="This mechanism already have his own standart_mechanism!")


def delete_standart_mechanism_m(id, db):
    get_in_db(db, Standart_mechanisms, id)
    db.query(Standart_mechanisms).filter(Standart_mechanisms.id == id).delete()
    db.commit()
