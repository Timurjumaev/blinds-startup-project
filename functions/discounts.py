from fastapi import HTTPException
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.discounts import Discounts


def all_discounts(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Discounts.type.like(search_formatted))
    else:
        search_filter = Discounts.id > 0
    discounts = db.query(Discounts).filter(search_filter).order_by(Discounts.type.asc())
    return pagination(discounts, page, limit)


def create_discount_t(form, db, thisuser):
    if form.type != "block_list" and form.type != "general" and form.type != "premium":
        raise HTTPException(status_code=400, detail="Discounts.type is error!")
    new_discount_db = Discounts(
        type=form.type,
        percent=form.percent,
        user_id=thisuser.id
    )
    save_in_db(db, new_discount_db)


def update_discount_t(form, db, thisuser):
    get_in_db(db, Discounts, form.id)
    if form.type != "block_list" and form.type != "general" and form.type != "premium":
        raise HTTPException(status_code=400, detail="Discounts.type is error!")

    db.query(Discounts).filter(Discounts.id == form.id).update({
        Discounts.type: form.type,
        Discounts.percent: form.percent,
        Discounts.user_id: thisuser.id
    })
    db.commit()


def delete_discount_t(id, db):
    if get_in_db(db, Discounts, id):
        db.query(Discounts).filter(Discounts.id == id).delete()
        db.commit()







