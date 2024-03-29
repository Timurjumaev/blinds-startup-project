from sqlalchemy.orm import joinedload
from models.mechanisms import Mechanisms
from models.trades import Trades
from models.warehouse_materials import Warehouse_materials
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.trade_mechanisms import Trade_mechanisms
from fastapi import HTTPException


def all_trade_mechanisms(search, page, limit, trade_id, db, thisuser):
    trade_mechanism = db.query(Trade_mechanisms).filter(Trade_mechanisms.branch_id == thisuser.branch_id).\
        options(joinedload(Trade_mechanisms.mechanism))
    search_formatted = "%{}%".format(search)
    search_filter = Mechanisms.name.like(search_formatted)
    if search and trade_id:
        trade_mechanism = trade_mechanism.filter(search_filter, Trade_mechanisms.trade_id == trade_id)\
            .order_by(Trade_mechanisms.id.asc())
    elif search is None and trade_id:
        trade_mechanism = trade_mechanism.filter(Trade_mechanisms.trade_id == trade_id)\
            .order_by(Trade_mechanisms.id.asc())
    elif trade_id is None and search:
        trade_mechanism = trade_mechanism.filter(search_filter).order_by(Trade_mechanisms.id.asc())
    else:
        trade_mechanism = trade_mechanism.order_by(Trade_mechanisms.id.asc())
    return pagination(trade_mechanism, page, limit)


def create_trade_mechanism_m(form, db, thisuser):
    the_one(db, Trades, form.trade_id, thisuser), the_one(db, Mechanisms, form.mechanism_id, thisuser)
    if db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == form.trade_id).first():
        raise HTTPException(status_code=400, detail="Bu mexanizmga standard mexanizm biriktirilgan!")
    if db.query(Warehouse_materials).filter(Warehouse_materials.mechanism_id == form.mechanism_id,
                                            Warehouse_materials.quantity >= form.quantity).first() is None:
        raise HTTPException(status_code=400, detail="Omborda bunday mexanizm yetarli emas!")
    new_trade_mechanism_db = Trade_mechanisms(
        trade_id=form.trade_id,
        mechanism_id=form.mechanism_id,
        quantity=form.quantity,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_trade_mechanism_db)
    db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                         Warehouse_materials.mechanism_id == form.mechanism_id).update({
        Warehouse_materials.quantity: Warehouse_materials.quantity - form.quantity
    })
    db.commit()


def update_trade_mechanism_m(form, db, thisuser):
    the_one(db, Trade_mechanisms, form.id, thisuser), the_one(db, Trades, form.trade_id, thisuser), \
        the_one(db, Mechanisms, form.mechanism_id, thisuser)
    tm = db.query(Trade_mechanisms).filter(Trade_mechanisms.id == form.id).first()
    if db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == form.trade_id).first() is None \
            or tm.trade_id == form.trade_id:
        old_trade_mechanism = db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == form.id).first()
        db.query(Trade_mechanisms).filter(Trade_mechanisms.id == form.id).update({
            Trade_mechanisms.trade_id: form.trade_id,
            Trade_mechanisms.mechanism_id: form.mechanism_id,
            Trade_mechanisms.quantity: form.quantity
        })
        db.commit()
        db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                             Warehouse_materials.mechanism_id == form.mechanism_id).update({
            Warehouse_materials.quantity: Warehouse_materials.quantity + old_trade_mechanism.quantity - form.quantity
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="This trade already have his own trade_mechanism!")


def delete_trade_mechanism_m(id, db, user):
    the_one(db, Trade_mechanisms, id, user)
    db.query(Trade_mechanisms).filter(Trade_mechanisms.id == id).delete()
    db.commit()

