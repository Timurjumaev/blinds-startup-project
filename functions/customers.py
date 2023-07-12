from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.phones import create_phone
from models.phones import Phones
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.customers import Customers


def all_customers(search, page, limit, db, user):
    customers = db.query(Customers).filter(Customers.branch_id == user.branch_id).options(joinedload(Customers.phones))
    if search:
        search_formatted = "%{}%".format(search)
        customers = customers.filter(Customers.name.like(search_formatted))
    customers = customers.order_by(Customers.name.asc())
    return pagination(customers, page, limit)


def one_customer(db, user, ident):
    the_customer = db.query(Customers).filter(Customers.branch_id == user.branch_id,
                                              Customers.id == ident).options(joinedload(Customers.phones)).first()
    if the_customer is None:
        raise HTTPException(status_code=404)
    return the_customer


def create_customer_r(form, db, thisuser):
    if form.type != "block_list" and form.type != "general" and form.type != "premium":
        raise HTTPException(status_code=400, detail="Customers.type is error!")
    new_customer_db = Customers(
        name=form.name,
        type=form.type,
        user_id=thisuser.id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_customer_db)
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, new_customer_db.id, thisuser.id, db, 'customer', thisuser.branch_id)


def update_customer_r(form, db, thisuser):
    the_one(db, Customers, form.id, thisuser), the_one(db, Phones, form.phones[0].id, thisuser)
    if form.type != "block_list" and form.type != "general" and form.type != "premium":
        raise HTTPException(status_code=400, detail="Customers.type error!")

    db.query(Customers).filter(Customers.id == form.id).update({
        Customers.name: form.name,
        Customers.type: form.type,
        Customers.user_id: thisuser.id
    })
    db.commit()
    phones = db.query(Phones).filter(Phones.source == "customer", Phones.source_id == form.id).all()
    for phone in phones:
        db.query(Phones).filter(Phones.id == phone.id).delete()
        db.commit()
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, form.id, thisuser.id, db, 'customer', thisuser.branch_id)






