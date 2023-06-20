from models.currencies import Currencies
from utils.db_operations import save_in_db, the_one


def create_currency_y(form, db, thisuser):
    new_currency_db = Currencies(
        price=form.price,
        currency=form.currency,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_currency_db)


def update_currency_y(form, db, user):
    the_one(db, Currencies, form.id, user)
    db.query(Currencies).filter(Currencies.id == form.id).update({
        Currencies.price: form.price,
        Currencies.currency: form.currency
    })
    db.commit()

