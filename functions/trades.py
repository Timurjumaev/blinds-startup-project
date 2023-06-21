from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.materials import Materials
from models.mechanisms import Mechanisms
from models.orders import Orders
from models.stages import Stages
from models.standart_mechanisms import Standart_mechanisms
from models.trade_mechanisms import Trade_mechanisms
from models.users import Users
from models.warehouse_materials import Warehouse_materials
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.trades import Trades


def all_trades(search, page, limit, order_id, stage_id, db, thisuser):
    trades = db.query(Trades).filter(Trades.branch_id == thisuser.branch_id).options(joinedload(Trades.user),
                                                                                     joinedload(Trades.material),
                                                                                     joinedload(Trades.stage),
                                                                                     joinedload(Trades.trade_mechanism))
    if order_id:
        order_filter = Trades.order_id == order_id
    else:
        order_filter = Trades.id > 0
    if stage_id:
        stage_filter = Trades.stage_id == stage_id
    else:
        stage_filter = Trades.id > 0
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Users.name.like(search_formatted)) | \
                        (Users.username.like(search_formatted)) | \
                        (Materials.name.like(search_formatted)) | \
                        (Stages.name.like(search_formatted))
    else:
        search_filter = Trades.id > 0
    trades = trades.filter(search_filter, order_filter, stage_filter).order_by(Trades.id.asc())
    return pagination(trades, page, limit)


def create_trade_e(form, db, thisuser):
    the_one(db, Materials, form.material_id, thisuser), the_one(db, Stages, form.stage_id, thisuser), \
        the_one(db, Orders, form.order_id, thisuser)
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
        order_id=form.order_id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_trade_db)
    material = the_one(db, Materials, form.material_id, thisuser)
    mechanisms_in_current_collaction = db.query(Mechanisms).filter(Mechanisms.collaction_id == material.collaction_id).all()
    for mechanism in mechanisms_in_current_collaction:
        standart_mechanism = db.query(Standart_mechanisms).filter(Standart_mechanisms.mechanism_id == mechanism.id).first()
        if standart_mechanism:
            new_trade_mechanism_db = Trade_mechanisms(
                trade_id=new_trade_db.id,
                mechanism_id=mechanism.id,
                quantity=standart_mechanism.quantity,
            )
            save_in_db(db, new_trade_mechanism_db)
            db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                                 Warehouse_materials.mechanism_id == mechanism.id).update({
                Warehouse_materials.quantity: Warehouse_materials.quantity - standart_mechanism.quantity
            })
            db.commit()


def update_trade_e(form, db, thisuser):
    the_one(db, Trades, form.id, thisuser), the_one(db, Materials, form.material_id, thisuser), \
        the_one(db, Stages, form.stage_id, thisuser), the_one(db, Orders, form.order_id, thisuser)
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
        material = the_one(db, Materials, form.material_id, thisuser)
        mechanisms_in_current_collaction = db.query(Mechanisms).filter(
            Mechanisms.collaction_id == material.collaction_id).all()
        for mechanism in mechanisms_in_current_collaction:
            standart_mechanism = db.query(Standart_mechanisms).filter(
                Standart_mechanisms.mechanism_id == mechanism.id).first()
            if standart_mechanism:
                old_trade_mechanism = db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == form.id).first()
                new_trade_mechanism_db = Trade_mechanisms(
                    trade_id=form.id,
                    mechanism_id=mechanism.id,
                    quantity=standart_mechanism.quantity,
                )
                save_in_db(db, new_trade_mechanism_db)
                db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                                     Warehouse_materials.mechanism_id == mechanism.id).update({
                    Warehouse_materials.quantity: Warehouse_materials.quantity + old_trade_mechanism.quantity - standart_mechanism.quantity
                })
                db.commit()

def delete_trade_e(id, db, user):
    the_one(db, Trades, id, user)
    db.query(Trades).filter(Trades.id == id).delete()
    db.commit()


def request_materials_s(form, db, thisuser):
    this_material = db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                                         Warehouse_materials.material_id == form.material_id,
                                                         Warehouse_materials.width > form.width,
                                                         Warehouse_materials.height > form.height).all()
    if this_material:
        return this_material
    raise HTTPException(status_code=400, detail="Bazada bunday o'lchamga mos material yo'q!")


def create_trade_material_s(form, db, thisuser):
    db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                         Warehouse_materials.id == form.warehouse_materials_id,
                                         Warehouse_materials.material_id == form.material_id).update({
        Warehouse_materials.width: Warehouse_materials.width - form.width,
        Warehouse_materials.height: Warehouse_materials.height - form.height
    })
    db.commit()
    raise HTTPException(status_code=200, detail="Successful!")


def update_trade_material_s(form, db, thisuser):
    old_trade = the_one(db, Trades, form.trade_id, thisuser)
    db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                         Warehouse_materials.id == form.warehouse_materials_id,
                                         Warehouse_materials.material_id == form.material_id).update({
        Warehouse_materials.width: Warehouse_materials.width + old_trade.width - form.width,
        Warehouse_materials.height: Warehouse_materials.height + old_trade.height - form.height
    })
    db.commit()
    raise HTTPException(status_code=200, detail="Successful!")




