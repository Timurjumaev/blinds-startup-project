from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.phones import create_phone, update_phone
from models.phones import Phones
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.branches import Branches


def all_branches(search, page, limit, db):
    warehouses = db.query(Branches).options(joinedload(Branches.phones))
    if search:
        search_formatted = "%{}%".format(search)
        warehouses = warehouses.filter(Branches.name.like(search_formatted))
    warehouses = warehouses.order_by(Branches.name.asc())
    return pagination(warehouses, page, limit)


def one_branch(db, ident):
    the_branch = db.query(Branches).filter(Branches.id == ident).options(joinedload(Branches.phones)).first()
    if the_branch is None:
        raise HTTPException(status_code=404)
    return the_branch


def create_branch_ch(form, db, thisuser):
    new_branch_db = Branches(
        name=form.name,
        address=form.address,
        map_long=form.map_long,
        map_lat=form.map_lat
    )
    save_in_db(db, new_branch_db)
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, new_branch_db.id, thisuser.id, db, 'branch', new_branch_db.id)


def update_branch_ch(form, db, thisuser):
    if get_in_db(db, Branches, form.id) is None\
            or get_in_db(db, Phones, form.phones[0].id) is None:
        raise HTTPException(status_code=400, detail="Branch or Phone not found!")

    db.query(Branches).filter(Branches.id == form.id).update({
        Branches.name: form.name,
        Branches.address: form.address,
        Branches.map_long: form.map_long,
        Branches.map_lat: form.map_lat
    })
    db.commit()

    for i in form.phones:
        phone_id = i.id
        comment = i.comment
        number = i.number
        update_phone(phone_id, comment, number, form.id, thisuser.id, db, 'branch')






