from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.notifications import manager
from models.collactions import Collactions
from models.materials import Materials
from models.mechanisms import Mechanisms
from models.orders import Orders
from models.stage_users import Stage_users
from models.stages import Stages
from models.standart_mechanisms import Standart_mechanisms
from models.trade_mechanisms import Trade_mechanisms
from models.user_balances import User_balances
from models.users import Users
from models.warehouse_materials import Warehouse_materials
from schemas.notifications import NotificationSchema
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.trades import Trades


def all_trades(search, page, limit, order_id, stage_id, db, arxiv, thisuser):
    trades = db.query(Trades)\
        .filter(Trades.branch_id == thisuser.branch_id)\
        .options(joinedload(Trades.user),
                 joinedload(Trades.material).options(joinedload(Materials.collaction).subqueryload(Collactions.category)),
                 joinedload(Trades.stage),
                 joinedload(Trades.trade_mechanism).options(joinedload(Trade_mechanisms.mechanism)))

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
    if arxiv:
        arxiv_filter = Trades.status == "done"
    else:
        arxiv_filter = Trades.status != "done"
    trades = trades.filter(search_filter, order_filter, stage_filter, arxiv_filter).order_by(Trades.id.desc())
    return pagination(trades, page, limit)


async def create_trade_e(form, db, thisuser):
    the_one(db, Materials, form.material_id, thisuser), the_one(db, Orders, form.order_id, thisuser)
    material = db.query(Materials).filter(Materials.id == form.material_id).first()
    store = db.query(Warehouse_materials).filter(Warehouse_materials.material_id == form.material_id).first()
    if store.width < form.width or store.height < form.height:
        raise HTTPException(status_code=400, detail="Siz tanlagan material yetarli emas!")
    this_order = db.query(Orders).filter(Orders.id == form.order_id).first()
    if this_order.status != "false":
        raise HTTPException(status_code=400, detail="Selected order already active!")
    stage = db.query(Stages).filter(Stages.number == 1).first()
    if stage is None:
        raise HTTPException(status_code=400, detail="Ishni boshlash uchun bosqich mavjud emas!")
    new_trade_db = Trades(
        material_id=form.material_id,
        width=form.width,
        height=form.height,
        stage_id=stage.id,
        status="false",
        comment=form.comment,
        user_id=thisuser.id,
        order_id=form.order_id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_trade_db)
    db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                         Warehouse_materials.material_id == form.material_id).update({
        Warehouse_materials.width: Warehouse_materials.width - form.width,
        Warehouse_materials.height: Warehouse_materials.height - form.height
    })
    db.commit()
    stage = db.query(Stages).filter(Stages.id == stage.id).first()
    stage_users = db.query(Stage_users).filter(Stage_users.stage_id == stage.id,
                                               Stage_users.branch_id == thisuser.branch_id).all()
    for stage_user in stage_users:
        user = db.query(Users).filter(Users.id == stage_user.user_id).first()
        data = NotificationSchema(
            title="Yangi ish!",
            body=f"Hurmatli foydalanuvchi {stage.name} bosqichiga yangi ish keldi!",
            user_id=user.id,
        )
        await manager.send_user(message=data, user_id=user.id, db=db)
    mechanisms_in_current_collaction = db.query(Mechanisms).filter(Mechanisms.collaction_id == material.collaction_id).all()
    for mechanism in mechanisms_in_current_collaction:
        standart_mechanism = db.query(Standart_mechanisms).filter(Standart_mechanisms.mechanism_id == mechanism.id).first()
        if standart_mechanism:
            warehouse_mechanism = db.query(Warehouse_materials).filter(
                Warehouse_materials.branch_id == thisuser.branch_id,
                Warehouse_materials.mechanism_id == mechanism.id).first()
            if warehouse_mechanism and warehouse_mechanism.quantity > standart_mechanism.quantity:
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


async def update_trade_e(form, db, thisuser):
    the_one(db, Materials, form.material_id, thisuser)
    the_one(db, Trades, form.id, thisuser), \
        the_one(db, Stages, form.stage_id, thisuser), the_one(db, Orders, form.order_id, thisuser)
    material = db.query(Materials).filter(Materials.id == form.material_id).first()
    old_trade = db.query(Trades).filter(Trades.id == form.id).first()
    if db.query(Trades).filter(Trades.id == form.id).first().status == "done":
        raise HTTPException(status_code=400, detail="This Trades.status is already 'done'!")
    if db.query(Trades).filter(Trades.id == form.id).first().status == "false" and form.status != "false" and form.status != "true":
        raise HTTPException(status_code=400, detail="This Trades.status is false, so updated_status is only false or true!")
    if db.query(Trades).filter(Trades.id == form.id).first().status == "true" and form.status != "false" and form.status != "true" and form.status != "done":
        raise HTTPException(status_code=400,
                            detail="Updated_status is only false, true or done!")
    db.query(Warehouse_materials).filter(Warehouse_materials.material_id == material.id).update({
        Warehouse_materials.width: Warehouse_materials.width + old_trade.width,
        Warehouse_materials.height: Warehouse_materials.height + old_trade.height
    })
    db.commit()
    store = db.query(Warehouse_materials).filter(Warehouse_materials.material_id == material.id).first()
    if store.width < form.width or store.height < form.height:
        raise HTTPException(status_code=400, detail="Siz tanlagan material yetarli emas!")
    this_stage = db.query(Stages).filter(Stages.id == form.stage_id).first()
    stage = db.query(Stages).filter(Stages.number > this_stage.number).first()
    if stage:
        finish = False
    else:
        finish = True
    db.query(Trades).filter(Trades.id == form.id).update({
        Trades.material_id: form.material_id,
        Trades.width: form.width,
        Trades.height: form.height,
        Trades.stage_id: form.stage_id,
        Trades.status: form.status,
        Trades.comment: form.comment,
        Trades.user_id: thisuser.id,
        Trades.finish: finish,
        Trades.order_id: form.order_id
    })
    db.commit()
    db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                         Warehouse_materials.material_id == form.material_id).update({
        Warehouse_materials.width: Warehouse_materials.width - form.width,
        Warehouse_materials.height: Warehouse_materials.height - form.height
    })
    db.commit()
    stage = db.query(Stages).filter(Stages.id == form.stage_id).first()
    stage_users = db.query(Stage_users).filter(Stage_users.stage_id == form.stage_id,
                                               Stage_users.branch_id == thisuser.branch_id).all()
    for stage_user in stage_users:
        user = db.query(Users).filter(Users.id == stage_user.user_id).first()
        data = NotificationSchema(
            title="Yangi ish!",
            body=f"Hurmatli foydalanuvchi {stage.name} bosqichiga yangi ish keldi!",
            user_id=user.id,
        )
        await manager.send_user(message=data, user_id=user.id, db=db)
    old_stage = db.query(Stages).filter(Stages.id == old_trade.stage_id).first()
    old_stage_users = db.query(Stage_users).filter(Stage_users.stage_id == old_stage.id).all()
    for i in old_stage_users:
        db.query(User_balances).filter(User_balances.currency_id == i.currency_id,
                                       User_balances.user_id == i.user_id).update({
            User_balances.balance: User_balances.balance + i.kpi
        })
        db.commit()
    if db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == form.id).first():
        mechanisms_in_current_collaction = db.query(Mechanisms).filter(
            Mechanisms.collaction_id == material.collaction_id).all()
        for mechanism in mechanisms_in_current_collaction:
            standart_mechanism = db.query(Standart_mechanisms).filter(
                Standart_mechanisms.mechanism_id == mechanism.id).first()
            if standart_mechanism:
                old_trade_mechanism = db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == form.id).first()
                db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                                     Warehouse_materials.mechanism_id == mechanism.id).update({
                    Warehouse_materials.quantity: Warehouse_materials.quantity + old_trade_mechanism.quantity
                })
                db.commit()
                db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == form.id).delete()
                db.commit()
                warehouse_mechanism = db.query(Warehouse_materials).filter(
                    Warehouse_materials.branch_id == thisuser.branch_id,
                    Warehouse_materials.mechanism_id == mechanism.id).first()
                if warehouse_mechanism and warehouse_mechanism.quantity > standart_mechanism.quantity:
                    new_trade_mechanism_db = Trade_mechanisms(
                        trade_id=form.id,
                        mechanism_id=mechanism.id,
                        quantity=standart_mechanism.quantity,
                    )
                    save_in_db(db, new_trade_mechanism_db)
                    db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                                         Warehouse_materials.mechanism_id == mechanism.id).update({
                        Warehouse_materials.quantity: Warehouse_materials.quantity - standart_mechanism.quantity
                    })
                    db.commit()


def delete_trade_e(id, db, user):
    the_one(db, Trades, id, user)
    trade = db.query(Trades).filter(Trades.id == id).first()
    material = db.query(Materials).filter(Materials.id == trade.material_id).first()
    db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == user.branch_id,
                                         Warehouse_materials.material_id == material.id).update({
        Warehouse_materials.width: Warehouse_materials.width + trade.width,
        Warehouse_materials.height: Warehouse_materials.height + trade.height
    })
    trade_mechanism = db.query(Trade_mechanisms).filter(Trade_mechanisms.trade_id == trade.id).first()
    if trade_mechanism:
        mechanism = db.query(Mechanisms).filter(Mechanisms.id == trade_mechanism.mechanism_id).first()
        db.query(Warehouse_materials).filter(Warehouse_materials.mechanism_id == mechanism.id).update({
            Warehouse_materials.quantity: Warehouse_materials.quantity + trade_mechanism.quantity
        })
    db.query(Trades).filter(Trades.id == id).delete()
    db.commit()


def request_materials_s(form, db, thisuser):
    this_material = db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id,
                                                         Warehouse_materials.material_id == form.material_id,
                                                         Warehouse_materials.width >= form.width,
                                                         Warehouse_materials.height >= form.height).all()
    if this_material:
        return this_material
    raise HTTPException(status_code=400, detail="Omborda bunday o'lchamga mos material yo'q!")


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


def one_trade(form, db, user):
    for i in form:
        trade = the_one(db, Trades, i.id, user)
        stage = db.query(Stages).filter(Stages.id == trade.stage_id).first()
        next_stage = db.query(Stages).filter(Stages.number == (stage.number + 1)).first()
        if next_stage is None:
            raise HTTPException(status_code=400, detail="Tanlangan savdo allaqachon oxirgi bosqichda yoki undan kiyingi bosqich mavjud emas!")
        this_stage = db.query(Stages).filter(Stages.number > next_stage.number).first()
        if this_stage:
            finish = False
        else:
            finish = True
        db.query(Trades).filter(Trades.id == trade.id).update({
            Trades.stage_id: next_stage.id,
            Trades.finish: finish
        })
        db.commit()






