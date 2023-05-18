from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.kassas import Kassas


def all_kassas(search, page, limit, db):
    kassas = db.query(Kassas).join(Kassas.currency).options(joinedload(Kassas.currency))
    if search:
        search_formatted = "%{}%".format(search)
        kassas = kassas.filter(Kassas.name.like(search_formatted) | Currencies.currency.like(search_formatted))
    kassas = kassas.order_by(Kassas.name.asc())
    return pagination(kassas, page, limit)


def create_kassa_a(form, db, thisuser):
    get_in_db(db, Currencies, form.currency_id)
    new_kassa_db = Kassas(
        name=form.name,
        comment=form.comment,
        balance=form.balance,
        currency_id=form.currency_id,
        user_id=thisuser.id
    )
    save_in_db(db, new_kassa_db)


def update_kassa_a(form, db, thisuser):
    get_in_db(db, Kassas, form.id), get_in_db(db, Currencies, form.currency_id)
    db.query(Kassas).filter(Kassas.id == form.id).update({
        Kassas.name: form.name,
        Kassas.comment: form.comment,
        Kassas.balance: form.balance,
        Kassas.currency_id: form.currency_id,
        Kassas.user_id: thisuser.id
    })
    db.commit()








