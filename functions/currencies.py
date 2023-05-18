from models.currencies import Currencies
from utils.db_operations import save_in_db, get_in_db


def create_currency_y(form, db):
        new_currency_db = Currencies(
            price=form.price,
            currency=form.currency
        )
        save_in_db(db, new_currency_db)





def update_currency_y(form, db):
    if get_in_db(db, Currencies, form.id):
        db.query(Currencies).filter(Currencies.id == form.id).update({
            Currencies.price: form.price,
            Currencies.currency: form.currency
        })
        db.commit()

