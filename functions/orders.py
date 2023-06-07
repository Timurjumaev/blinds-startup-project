from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.customers import Customers
from models.users import Users
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.orders import Orders


def all_orders(search, page, limit, customer_id, db):
    orders = db.query(Orders).options(joinedload(Orders.customer),
                                      joinedload(Orders.user))
    search_formatted = "%{}%".format(search)
    search_filter = Users.name.like(search_formatted) | Users.username.like(search_formatted) | Customers.name.like(search_formatted)
    if search and customer_id:
        orders = orders.filter(search_filter, Orders.customer_id == customer_id).order_by(Orders.id.asc())
    elif search is None and customer_id:
        orders = orders.filter(Orders.customer_id == customer_id).order_by(Orders.id.asc())
    elif customer_id is None and search:
        orders = orders.filter(search_filter).order_by(Orders.id.asc())
    else:
        orders = orders.order_by(Orders.id.asc())
    return pagination(orders, page, limit)


def create_order_r(form, db, thisuser):
    get_in_db(db, Customers, form.customer_id)
    new_order_db = Orders(
        time=datetime.now(),
        customer_id=form.customer_id,
        discount=form.discount,
        status="false",
        user_id=thisuser.id,
        delivery_date=form.delivery_date
    )
    save_in_db(db, new_order_db)


def update_order_r(form, db, thisuser):
    get_in_db(db, Orders, form.id), get_in_db(db, Customers, form.customer_id)
    if db.query(Orders).filter(Orders.id == form.id).first().status == "done":
        raise HTTPException(status_code=400, detail="This Orders.status is already 'done'!")
    if db.query(Orders).filter(Orders.id == form.id).first().status == "false" and form.status != "false" and form.status != "true":
        raise HTTPException(status_code=400, detail="This Orders.status is false, so updated_status is only false or true!")
    if db.query(Orders).filter(Orders.id == form.id).first().status == "true" and form.status != "false" and form.status != "true" and form.status != "done":
        raise HTTPException(status_code=400,
                            detail="Updated_status is only false, true or done!")
    db.query(Orders).filter(Orders.id == form.id).update({
        Orders.customer_id: form.customer_id,
        Orders.discount: form.discount,
        Orders.status: form.status,
        Orders.user_id: thisuser.id,
        Orders.delivery_date: form.delivery_date
    })
    db.commit()


def delete_order_r(id, db):
    get_in_db(db, Orders, id)
    db.query(Orders).filter(Orders.id == id).delete()
    db.commit()







