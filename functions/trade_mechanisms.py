from sqlalchemy.orm import joinedload
from models.mechanisms import Mechanisms
from models.trades import Trades
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.trade_mechanisms import Trade_mechanisms
from fastapi import HTTPException


def all_trade_mechanisms(search, page, limit, db):
    trade_mechanism = db.query(Trade_mechanisms).options(joinedload(Trade_mechanisms.mechanism))
    if search:
        search_formatted = "%{}%".format(search)
        trade_mechanism = trade_mechanism.filter(Mechanisms.name.like(search_formatted))
    trade_mechanism = trade_mechanism.order_by(Trade_mechanisms.id.asc())
    return pagination(trade_mechanism, page, limit)


def create_trade_mechanism_m(form, db):
    get_in_db(db, Trades, form.trade_id), get_in_db(db, Mechanisms, form.mechanism_id)
    if db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == form.trade_id).first():
        raise HTTPException(status_code=400, detail="This trade already have his own trade_mechanism!")
    new_trade_mechanism_db = Trade_mechanisms(
        trade_id=form.trade_id,
        mechanism_id=form.mechanism_id,
        width=form.width,
        quantity=form.quantity
    )
    save_in_db(db, new_trade_mechanism_db)


def update_trade_mechanism_m(form, db):
    get_in_db(db, Trade_mechanisms, form.id), get_in_db(db, Trades, form.trade_id), \
        get_in_db(db, Mechanisms, form.mechanism_id)
    tm = db.query(Trade_mechanisms).filter(Trade_mechanisms.id == form.id).first()
    if db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == form.trade_id).first() is None \
            or tm.trade_id == form.trade_id:
        db.query(Trade_mechanisms).filter(Trade_mechanisms.id == form.id).update({
            Trade_mechanisms.trade_id: form.trade_id,
            Trade_mechanisms.mechanism_id: form.mechanism_id,
            Trade_mechanisms.width: form.width,
            Trade_mechanisms.quantity: form.quantity
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="This trade already have his own trade_mechanism!")


def delete_trade_mechanism_m(id, db):
    get_in_db(db, Trade_mechanisms, id)
    db.query(Trade_mechanisms).filter(Trade_mechanisms.id == id).delete()
    db.commit()

