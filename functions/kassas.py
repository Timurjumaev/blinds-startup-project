from sqlalchemy.orm import joinedload
from models.currencies import Currencies
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.kassas import Kassas


def all_kassas(search, page, limit, db, thisuser):
    kassas = db.query(Kassas).filter(Kassas.branch_id == thisuser.branch_id).options(joinedload(Kassas.currency))
    if search:
        search_formatted = "%{}%".format(search)
        kassas = kassas.filter(Kassas.name.like(search_formatted) | Currencies.currency.like(search_formatted))
    kassas = kassas.order_by(Kassas.name.asc())
    return pagination(kassas, page, limit)


def create_kassa_a(form, db, thisuser):
    the_one(db, Currencies, form.currency_id, thisuser)
    new_kassa_db = Kassas(
        name=form.name,
        balance=0,
        currency_id=form.currency_id,
        user_id=thisuser.id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_kassa_db)


def update_kassa_a(form, db, thisuser):
    the_one(db, Kassas, form.id, thisuser)
    db.query(Kassas).filter(Kassas.id == form.id).update({
        Kassas.name: form.name,
        Kassas.user_id: thisuser.id
    })
    db.commit()








