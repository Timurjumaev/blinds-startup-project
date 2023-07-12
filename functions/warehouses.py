from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.phones import create_phone
from models.phones import Phones
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.warehouses import Warehouses


def all_warehouses(search, page, limit, db, thisuser):
    warehouses = db.query(Warehouses).filter(Warehouses.branch_id == thisuser.branch_id).\
        options(joinedload(Warehouses.phones))
    if search:
        search_formatted = "%{}%".format(search)
        warehouses = warehouses.filter(Warehouses.name.like(search_formatted))
    warehouses = warehouses.order_by(Warehouses.name.asc())
    return pagination(warehouses, page, limit)


def one_warehouse(db, user, ident):
    the_warehouse = db.query(Warehouses).filter(Warehouses.branch_id == user.branch_id,
                                                Warehouses.id == ident).options(joinedload(Warehouses.phones)).first()
    if the_warehouse is None:
        raise HTTPException(status_code=404)
    return the_warehouse


def create_warehouse_e(form, db, thisuser):
    new_warehouse_db = Warehouses(
        name=form.name,
        address=form.address,
        map_long=form.map_long,
        map_lat=form.map_lat,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_warehouse_db)
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, new_warehouse_db.id, thisuser.id, db, 'warehouse', thisuser.branch_id)


def update_warehouse_e(form, db, thisuser):
    the_one(db, Warehouses, form.id, thisuser), the_one(db, Phones, form.phones[0].id, thisuser)
    db.query(Warehouses).filter(Warehouses.id == form.id).update({
        Warehouses.name: form.name,
        Warehouses.address: form.address,
        Warehouses.map_long: form.map_long,
        Warehouses.map_lat: form.map_lat
    })
    db.commit()
    phones = db.query(Phones).filter(Phones.source == "warehouse", Phones.source_id == form.id).all()
    for phone in phones:
        db.query(Phones).filter(Phones.id == phone.id).delete()
        db.commit()
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, form.id, thisuser.id, db, 'warehouse', thisuser.branch_id)






