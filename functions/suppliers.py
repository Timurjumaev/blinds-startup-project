from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones import create_phone, update_phone
from models.phones import Phones
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.suppliers import Suppliers


def all_suppliers(search, page, limit, db, thisuser):
    suppliers = db.query(Suppliers).filter(Suppliers.branch_id == thisuser.branch_id).\
        options(joinedload(Suppliers.phones))
    if search:
        search_formatted = "%{}%".format(search)
        suppliers = suppliers.filter(Suppliers.name.like(search_formatted))
    suppliers = suppliers.order_by(Suppliers.name.asc())
    return pagination(suppliers, page, limit)


def create_supplier_r(form, db, thisuser):
    new_supplier_db = Suppliers(
        name=form.name,
        address=form.address,
        map_long=form.map_long,
        map_lat=form.map_lat,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_supplier_db)
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, new_supplier_db.id, thisuser.id, db, 'supplier', thisuser.branch_id)


def update_supplier_r(form, db, thisuser):
    the_one(db, Suppliers, form.id, thisuser), the_one(db, Phones, form.phones[0].id, thisuser)
    db.query(Suppliers).filter(Suppliers.id == form.id).update({
        Suppliers.name: form.name,
        Suppliers.address: form.address,
        Suppliers.map_long: form.map_long,
        Suppliers.map_lat: form.map_lat
    })
    db.commit()

    for i in form.phones:
        phone_id = i.id
        comment = i.comment
        number = i.number
        update_phone(phone_id, comment, number, form.id, thisuser.id, db, 'supplier')






