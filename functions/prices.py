from sqlalchemy.orm import joinedload
from models.collactions import Collactions
from models.currencies import Currencies
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.prices import Prices


def all_prices(page, limit, collaction_id, db, thisuser):
    if collaction_id:
        prices = db.query(Prices).filter(Prices.collaction_id == collaction_id, Prices.branch_id == thisuser.branch_id)
    else:
        prices = db.query(Prices).filter(Prices.branch_id == thisuser.branch_id)
    prices = prices.options(joinedload(Prices.currency)).order_by(Prices.price.asc())
    return pagination(prices, page, limit)


def create_price_e(form, db, thisuser):
    the_one(db, Collactions, form.collaction_id, thisuser), the_one(db, Currencies, form.currency_id, thisuser)
    new_price_db = Prices(
        price=form.price,
        currency_id=form.currency_id,
        width1=form.width1,
        width2=form.width2,
        height1=form.height1,
        height2=form.height2,
        collaction_id=form.collaction_id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_price_db)


def update_price_e(form, db, user):
    the_one(db, Prices, form.id, user), the_one(db, Collactions, form.collaction_id, user), \
        the_one(db, Currencies, form.currency_id, user)
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

