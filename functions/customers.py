from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones import create_phone, update_phone
from models.phones import Phones
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.customers import Customers


def all_customers(search, page, limit, db):
    customers = db.query(Customers).join(Customers.phones).options(joinedload(Customers.phones))
    if search:
        search_formatted = "%{}%".format(search)
        customers = customers.filter(Customers.name.like(search_formatted))
    customers = customers.order_by(Customers.name.asc())
    return pagination(customers, page, limit)


def create_customer_r(form, db, thisuser):
    if form.type != "block_list" and form.type != "general" and form.type != "premium":
        raise HTTPException(status_code=400, detail="Customers.type is error!")
    new_customer_db = Customers(
        name=form.name,
        type=form.type,
        user_id=thisuser.id
    )
    save_in_db(db, new_customer_db)
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, new_customer_db.id, thisuser.id, db, 'customer')


def update_customer_r(form, db, thisuser):
    get_in_db(db, Customers, form.id), get_in_db(db, Phones, form.phones[0].id)
    if form.type != "block_list" and form.type != "general" and form.type != "premium":
        raise HTTPException(status_code=400, detail="Customers.type error!")

    db.query(Customers).filter(Customers.id == form.id).update({
        Customers.name: form.name,
        Customers.type: form.type,
        Customers.user_id: thisuser.id
    })
    db.commit()

    for i in form.phones:
        phone_id = i.id
        comment = i.comment
        number = i.number
        update_phone(phone_id, comment, number, form.id, thisuser.id, db, 'customer')





