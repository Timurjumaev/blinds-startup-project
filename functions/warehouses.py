from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.phones import create_phone, update_phone
from models.phones import Phones
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.warehouses import Warehouses


def all_warehouses(search, page, limit, db):
    warehouses = db.query(Warehouses).join(Warehouses.phones).options(joinedload(Warehouses.phones))
    if search:
        search_formatted = "%{}%".format(search)
        warehouses = warehouses.filter(Warehouses.name.like(search_formatted))
    warehouses = warehouses.order_by(Warehouses.name.asc())
    return pagination(warehouses, page, limit)


def create_warehouse_e(form, db, thisuser):
    new_warehouse_db = Warehouses(
        name=form.name,
        address=form.address,
        map_long=form.map_long,
        map_lat=form.map_lat
    )
    save_in_db(db, new_warehouse_db)
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, new_warehouse_db.id, thisuser.id, db, 'warehouse')


def update_warehouse_e(form, db, thisuser):
    if get_in_db(db, Warehouses, form.id) is None\
            or get_in_db(db, Phones, form.phones[0].id) is None:
        raise HTTPException(status_code=400, detail="Warehouse or Phone not found!")

    db.query(Warehouses).filter(Warehouses.id == form.id).update({
        Warehouses.name: form.name,
        Warehouses.address: form.address,
        Warehouses.map_long: form.map_long,
        Warehouses.map_lat: form.map_lat
    })
    db.commit()

    for i in form.phones:
        phone_id = i.id
        comment = i.comment
        number = i.number
        update_phone(phone_id, comment, number, form.id, thisuser.id, db, 'warehouse')






