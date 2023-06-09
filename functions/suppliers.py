from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones import create_phone
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


def one_supplier(db, user, ident):
    the_supplier = db.query(Suppliers).filter(Suppliers.branch_id == user.branch_id,
                                              Suppliers.id == ident).options(joinedload(Suppliers.phones)).first()
    if the_supplier is None:
        raise HTTPException(status_code=404)
    return the_supplier


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
    the_one(db, Suppliers, form.id, thisuser)
    db.query(Suppliers).filter(Suppliers.id == form.id).update({
        Suppliers.name: form.name,
        Suppliers.address: form.address,
        Suppliers.map_long: form.map_long,
        Suppliers.map_lat: form.map_lat
    })
    db.commit()
    phones = db.query(Phones).filter(Phones.source == "supplier", Phones.source_id == form.id).all()
    for phone in phones:
        db.query(Phones).filter(Phones.id == phone.id).delete()
        db.commit()
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, form.id, thisuser.id, db, 'supplier', thisuser.branch_id)






