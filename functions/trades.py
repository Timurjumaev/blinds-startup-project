from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.materials import Materials
from models.mechanisms import Mechanisms
from models.orders import Orders
from models.stages import Stages
from models.standart_mechanisms import Standart_mechanisms
from models.trade_mechanisms import Trade_mechanisms
from models.users import Users
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.trades import Trades


def all_trades(search, page, limit, db):
    trades = db.query(Trades).options(joinedload(Trades.user),
                                      joinedload(Trades.material),
                                      (joinedload(Trades.stage)))
    if search:
        search_formatted = "%{}%".format(search)
        trades = trades.filter((Users.name.like(search_formatted)) |
                               (Users.username.like(search_formatted)) |
                               (Materials.name.like(search_formatted)) |
                               (Stages.name.like(search_formatted)))
    trades = trades.order_by(Trades.id.asc())
    return pagination(trades, page, limit)


def create_trade_e(form, db, thisuser):
    get_in_db(db, Materials, form.material_id), get_in_db(db, Stages, form.stage_id), get_in_db(db, Orders, form.order_id)
    this_order = db.query(Orders).filter(Orders.id == form.order_id).first()
    if this_order.status != "false":
        raise HTTPException(status_code=400, detail="Selected order already active!")
    new_trade_db = Trades(
        material_id=form.material_id,
        width=form.width,
        height=form.height,
        stage_id=form.stage_id,
        status="false",
        comment=form.comment,
        user_id=thisuser.id,
        order_id=form.order_id
    )
    save_in_db(db, new_trade_db)
    material = get_in_db(db, Materials, form.material_id)
    mechanisms_in_current_collaction = db.query(Mechanisms).filter(Mechanisms.collaction_id == material.collaction_id).all()
    for mechanism in mechanisms_in_current_collaction:
        standart_mechanism = db.query(Standart_mechanisms).filter(Standart_mechanisms.mechanism_id == mechanism.id).first()
        if standart_mechanism:
            new_trade_mechanism_db = Trade_mechanisms(
                trade_id=new_trade_db.id,
                mechanism_id=mechanism.id,
                width=standart_mechanism.width,
                quantity=standart_mechanism.quantity,
            )
            save_in_db(db, new_trade_mechanism_db)


def update_trade_e(form, db, thisuser):
    get_in_db(db, Trades, form.id), get_in_db(db, Materials, form.material_id), \
        get_in_db(db, Stages, form.stage_id), get_in_db(db, Orders, form.order_id)
    if db.query(Trades).filter(Trades.id == form.id).first().status == "done":
        raise HTTPException(status_code=400, detail="This Trades.status is already 'done'!")
    if db.query(Trades).filter(Trades.id == form.id).first().status == "false" and form.status != "false" and form.status != "true":
        raise HTTPException(status_code=400, detail="This Trades.status is false, so updated_status is only false or true!")
    if db.query(Trades).filter(Trades.id == form.id).first().status == "true" and form.status != "false" and form.status != "true" and form.status != "done":
        raise HTTPException(status_code=400,
                            detail="Updated_status is only false, true or done!")
    db.query(Trades).filter(Trades.id == form.id).update({
        Trades.material_id: form.material_id,
        Trades.width: form.width,
        Trades.height: form.height,
        Trades.stage_id: form.stage_id,
        Trades.status: form.status,
        Trades.comment: form.comment,
        Trades.user_id: thisuser.id,
        Trades.order_id: form.order_id
    })
    db.commit()
    if db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == form.id).first():
        db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == form.id).delete()
        db.commit()
        material = get_in_db(db, Materials, form.material_id)
        mechanisms_in_current_collaction = db.query(Mechanisms).filter(
            Mechanisms.collaction_id == material.collaction_id).all()
        for mechanism in mechanisms_in_current_collaction:
            standart_mechanism = db.query(Standart_mechanisms).filter(
                Standart_mechanisms.mechanism_id == mechanism.id).first()
            if standart_mechanism:
                new_trade_mechanism_db = Trade_mechanisms(
                    trade_id=form.id,
                    mechanism_id=mechanism.id,
                    width=standart_mechanism.width,
                    quantity=standart_mechanism.quantity,
                )
                save_in_db(db, new_trade_mechanism_db)


def delete_trade_e(id, db):
    get_in_db(db, Trades, id)
    db.query(Trades).filter(Trades.id == id).delete()
    db.commit()
