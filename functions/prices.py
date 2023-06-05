from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

from models.collactions import Collactions
from models.currencies import Currencies
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.prices import Prices


def all_prices(page, limit, collaction_id, db):
    if collaction_id:
        prices = db.query(Prices).filter(Prices.collaction_id == collaction_id)
    else:
        prices = db.query(Prices)
    prices = prices.options(joinedload(Prices.currency)).order_by(Prices.price.asc())
    return pagination(prices, page, limit)


def create_price_e(form, db):
    if get_in_db(db, Collactions, form.collaction_id) and get_in_db(db, Currencies, form.currency_id):
        new_price_db = Prices(
            price=form.price,
            currency_id=form.currency_id,
            width1=form.width1,
            width2=form.width2,
            height1=form.height1,
            height2=form.height2,
            collaction_id=form.collaction_id
        )
        save_in_db(db, new_price_db)


def update_price_e(form, db):
    if get_in_db(db, Prices, form.id) and get_in_db(db, Collactions, form.collaction_id) and get_in_db(db, Currencies, form.currency_id):
        db.query(Prices).filter(Prices.id == form.id).update({
            Prices.price: form.price,
            Prices.currency_id: form.currency_id,
            Prices.width1: form.width1,
            Prices.width2: form.width2,
            Prices.height1: form.height1,
            Prices.height2: form.height2,
            Prices.collaction_id: form.collaction_id
        })
        db.commit()

