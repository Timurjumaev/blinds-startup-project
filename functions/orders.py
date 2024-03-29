from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.notifications import manager
from models.collactions import Collactions
from models.currencies import Currencies
from models.customers import Customers
from models.discounts import Discounts
from models.incomes import Incomes
from models.kassas import Kassas
from models.loans import Loans
from models.materials import Materials
from models.prices import Prices
from models.trades import Trades
from models.users import Users
from schemas.notifications import NotificationSchema
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.orders import Orders
from sqlalchemy.sql import label, func


def all_orders(search, page, limit, customer_id, db, thisuser, archive):
    orders = db.query(Orders).filter(Orders.branch_id == thisuser.branch_id).options(joinedload(Orders.customer),
                                                                                     joinedload(Orders.user))
    if archive == "yes":
        orders = orders.filter(Orders.status == "done")
    elif archive == "no":
        orders = orders.filter(Orders.status != "done")
    elif archive is None:
        orders = orders
    else:
        raise HTTPException(status_code=400, detail="Bor yoqal!!!")
    search_formatted = "%{}%".format(search)
    search_filter = Users.name.like(search_formatted) | \
                    Users.username.like(search_formatted) | \
                    Customers.name.like(search_formatted)
    if search and customer_id:
        orders = orders.filter(search_filter, Orders.customer_id == customer_id).order_by(Orders.id.asc())
    elif search is None and customer_id:
        orders = orders.filter(Orders.customer_id == customer_id).order_by(Orders.id.asc())
    elif customer_id is None and search:
        orders = orders.filter(search_filter).order_by(Orders.id.asc())
    else:
        orders = orders.order_by(Orders.delivery_date.desc())
    return pagination(orders, page, limit)


def one_order_r(order_id, db, thisuser):
    this_order = the_one(db, Orders, order_id, thisuser)
    trades = db.query(Trades).filter(Trades.order_id == order_id).all()
    money = 0
    for trade in trades:
        material = db.query(Materials).filter(Materials.id == trade.material_id).first()
        collaction = db.query(Collactions).filter(Collactions.id == material.collaction_id).first()
        price = db.query(Prices).filter(Prices.collaction_id == collaction.id,
                                        Prices.width1 <= trade.width,
                                        Prices.width2 >= trade.width,
                                        Prices.height1 <= trade.height,
                                        Prices.height2 >= trade.height).first()
        if price:
            this_money = price.price
            this_currency = db.query(Currencies).filter(Currencies.id == price.currency_id).first()
            this_money = this_money * this_currency.price
            money = money + this_money
        else:
            raise HTTPException(status_code=400, detail="Ushbu o'lchamdagi material tegishli bo'lgan kolleksiyaga hali narx belgilanmagan!")
    total_money = money - this_order.discount
    customer = db.query(Customers).filter(Customers.id == Orders.customer_id).first()
    discount = db.query(Discounts).filter(Discounts.type == customer.type).first()
    if discount:
        discount_sum = total_money * discount.percent / 100
    else:
        discount_sum = 0
    total_sum = db.query(func.coalesce(func.sum(Incomes.money), 0)).filter(
            Incomes.source == "order",
            Incomes.source_id == order_id
        ).scalar()
    return {"order": this_order,
            "money": total_money,
            "incomes": total_sum,
            "discount": discount_sum}


def create_order_r(form, db, thisuser):
    the_one(db, Customers, form.customer_id, thisuser)
    new_order_db = Orders(
        time=datetime.now(),
        customer_id=form.customer_id,
        status="false",
        user_id=thisuser.id,
        delivery_date=form.delivery_date,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_order_db)


async def update_order_r(form, db, thisuser):
    the_one(db, Orders, form.id, thisuser), the_one(db, Customers, form.customer_id, thisuser)
    users = db.query(Users).filter(Users.status, Users.branch_id == thisuser.branch_id, Users.role == "admin").all()
    if db.query(Orders).filter(Orders.id == form.id).first().status == "done":
        raise HTTPException(status_code=400, detail="This Orders.status is already 'done'!")
    if db.query(Orders).filter(Orders.id == form.id).first().status == "false" and form.status != "false" and form.status != "true":
        raise HTTPException(status_code=400, detail="This Orders.status is false, so updated_status is only false or true!")
    if db.query(Orders).filter(Orders.id == form.id).first().status == "true" and form.status != "false" and form.status != "true" and form.status != "done":
        raise HTTPException(status_code=400,
                            detail="Updated_status is only false, true or done!")
    if form.status != "false" and db.query(Trades).filter(Trades.order_id == form.id).first() is None:
        raise HTTPException(status_code=400, detail="Ushbu buyurtmada savdo mavjud emas!")
    old_order = db.query(Orders).filter(Orders.id == form.id).first()
    db.query(Orders).filter(Orders.id == form.id).update({
        Orders.customer_id: form.customer_id,
        Orders.status: form.status,
        Orders.user_id: thisuser.id,
        Orders.delivery_date: form.delivery_date,
        Orders.discount: form.discount
    })
    db.commit()
    this_customer = db.query(Customers).filter(Customers.id == form.customer_id).first()
    trades = db.query(Trades).filter(Trades.order_id == form.id).all()
    if form.status == "true":
        for trade in trades:
            db.query(Trades).filter(Trades.id == trade.id).update({
                Trades.status: form.status
            })
            db.commit()
        if old_order.status == "false":
            for user in users:
                data = NotificationSchema(
                    title="Yangi buyurtma!",
                    body=f"Hurmatli foydalanuvchi {this_customer.name} ismli mijozdan buyurtma olindi!",
                    user_id=user.id,
                )
                await manager.send_user(message=data, user_id=user.id, db=db)
    if form.status == "done":
        for trade in trades:
            db.query(Trades).filter(Trades.id == trade.id).update({
                Trades.status: form.status
            })
            db.commit()
        for user in users:
            data = NotificationSchema(
                title="Yakunlangan buyurtma!",
                body=f"Hurmatli foydalanuvchi {this_customer.name} ismli mijozning buyurtmasi yakunlandi!",
                user_id=user.id,
            )
            await manager.send_user(message=data, user_id=user.id, db=db)
        if form.kassa_id != 0:
            kassa = the_one(db, Kassas, form.kassa_id, thisuser)
            currency = db.query(Currencies).filter(Currencies.currency == "so'm").first()
            if currency is None:
                raise HTTPException(status_code=400, detail="so'mlik valyuta mavjud emas!")
            if kassa.currency_id != currency.id:
                raise HTTPException(status_code=400, detail="Tanlangan kassaning valyutasi so'm emas!")
            a = one_order_r(form.id, db, thisuser)
            if form.summa > a["money"] - a["incomes"]:
                raise HTTPException(status_code=400, detail="Kiritilayotgan pul qoldiq summadan katta!")
            elif form.summa == a["money"] - a["incomes"]:
                income_db = Incomes(
                    money=form.summa,
                    currency_id=currency.id,
                    source="order",
                    source_id=form.id,
                    time=datetime.now(),
                    user_id=thisuser.id,
                    kassa_id=form.kassa_id,
                    comment=form.comment,
                    updelstatus=True,
                    branch_id=thisuser.branch_id
                )
                save_in_db(db, income_db)
                db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
                    Kassas.balance: Kassas.balance + form.summa
                })
                db.commit()
            elif 0 < form.summa < a["money"] - a["incomes"]:
                income_db = Incomes(
                    money=form.summa,
                    currency_id=currency.id,
                    source="order",
                    source_id=form.id,
                    time=datetime.now(),
                    user_id=thisuser.id,
                    kassa_id=form.kassa_id,
                    comment=form.comment,
                    updelstatus=True,
                    branch_id=thisuser.branch_id
                )
                save_in_db(db, income_db)
                loan = Loans(
                    money=a["money"] - a["incomes"] - form.summa,
                    currency_id=currency.id,
                    residual=a["money"] - a["incomes"] - form.summa,
                    order_id=form.id,
                    return_date=form.return_date,
                    comment=form.comment,
                    status=False,
                    branch_id=thisuser.branch_id
                )
                save_in_db(db, loan)
                db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
                    Kassas.balance: Kassas.balance + form.summa
                })
                db.commit()
            else:
                loan = Loans(
                    money=a["money"] - a["incomes"],
                    currency_id=currency.id,
                    residual=a["money"] - a["incomes"],
                    order_id=form.id,
                    return_date=form.return_date,
                    comment=form.comment,
                    status=False,
                    branch_id=thisuser.branch_id
                )
                save_in_db(db, loan)


def delete_order_r(id, db, user):
    order = the_one(db, Orders, id, user)
    if order.status != "false":
        raise HTTPException(status_code=400, detail="Ushbu buyurtma allaqachon tasdiqlangan!")
    db.query(Orders).filter(Orders.id == id).delete()
    trades = db.query(Trades).filter(Trades.order_id == id).all()
    db.commit()
    for trade in trades:
        db.query(Trades).filter(Trades.id == trade.id).delete()
        db.commit()







