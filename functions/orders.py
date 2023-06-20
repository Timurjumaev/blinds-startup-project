from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.collactions import Collactions
from models.currencies import Currencies
from models.customers import Customers
from models.discounts import Discounts
from models.incomes import Incomes
from models.materials import Materials
from models.prices import Prices
from models.trades import Trades
from models.users import Users
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.orders import Orders


def all_orders(search, page, limit, customer_id, db, thisuser):
    orders = db.query(Orders).filter(Orders.branch_id == thisuser.branch_id).options(joinedload(Orders.customer),
                                                                                     joinedload(Orders.user))
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
        orders = orders.order_by(Orders.id.asc())
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
    this_customer = db.query(Customers).filter(Customers.id == this_order.customer_id).first()
    this_discount = db.query(Discounts).filter(Discounts.type == this_customer.type).first()
    if this_discount is None:
        raise HTTPException(status_code=400, detail="Mijozni turiga teng bolgan turdagi chegirma topilmadi!")
    total_discount = (money * this_discount.percent) / 100
    total_money = money - total_discount
    this_income = db.query(Incomes).filter(Incomes.source == "order", Incomes.source_id == this_order.id).first()
    if this_income:
        db.query(Orders).filter(Orders.id == this_order.id).update({
            Orders.income_status: False
        })
        db.commit()
    return (this_order,
            {"money": total_money})


def create_order_r(form, db, thisuser):
    the_one(db, Customers, form.customer_id, thisuser)
    new_order_db = Orders(
        time=datetime.now(),
        customer_id=form.customer_id,
        status="false",
        user_id=thisuser.id,
        delivery_date=form.delivery_date,
        income_status=True,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_order_db)


def update_order_r(form, db, thisuser):
    the_one(db, Orders, form.id, thisuser), the_one(db, Customers, form.customer_id, thisuser)
    if db.query(Orders).filter(Orders.id == form.id).first().status == "done":
        raise HTTPException(status_code=400, detail="This Orders.status is already 'done'!")
    if db.query(Orders).filter(Orders.id == form.id).first().status == "false" and form.status != "false" and form.status != "true":
        raise HTTPException(status_code=400, detail="This Orders.status is false, so updated_status is only false or true!")
    if db.query(Orders).filter(Orders.id == form.id).first().status == "true" and form.status != "false" and form.status != "true" and form.status != "done":
        raise HTTPException(status_code=400,
                            detail="Updated_status is only false, true or done!")
    db.query(Orders).filter(Orders.id == form.id).update({
        Orders.customer_id: form.customer_id,
        Orders.status: form.status,
        Orders.user_id: thisuser.id,
        Orders.delivery_date: form.delivery_date
    })
    db.commit()


def delete_order_r(id, db, user):
    the_one(db, Orders, id, user)
    db.query(Orders).filter(Orders.id == id).delete()
    db.commit()







