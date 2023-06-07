from fastapi import HTTPException
from utils.db_operations import save_in_db, get_in_db
from models.discounts import Discounts


def create_discount_t(form, db, thisuser):
    if form.type != "general" and form.type != "premium":
        raise HTTPException(status_code=400, detail="Discounts.type is error!")
    if db.query(Discounts).filter(Discounts.type == form.type).first():
        raise HTTPException(status_code=400, detail="This type of discount already created!")
    new_discount_db = Discounts(
        type=form.type,
        percent=form.percent,
        user_id=thisuser.id
    )
    save_in_db(db, new_discount_db)


def delete_discount_t(id, db):
    if get_in_db(db, Discounts, id):
        db.query(Discounts).filter(Discounts.id == id).delete()
        db.commit()







