from datetime import datetime, timedelta

from fastapi import HTTPException

from models.currencies import Currencies
from models.customers import Customers
from models.kassas import Kassas
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.incomes import Incomes


def all_incomes(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Incomes.money.like(search_formatted))
    else:
        search_filter = Incomes.id > 0
    incomes = db.query(Incomes).filter(search_filter).order_by(Incomes.money.asc())
    return pagination(incomes, page, limit)


def create_income_e(form, db, thisuser):
    get_in_db(db, Currencies, form.currency_id), get_in_db(db, Kassas, form.kassa_id)
    if db.query(Kassas).filter(Kassas.currency_id == form.currency_id).first() is None:
        raise HTTPException(status_code=400, detail="Current currency_id != Kassas.currency_id")
    if get_in_db(db, Customers, form.source_id) and form.source == "customer":
        new_income_db = Incomes(
            money=form.money,
            currency_id=form.currency_id,
            source=form.source,
            source_id=form.source_id,
            time=datetime.now(),
            user_id=thisuser.id,
            kassa_id=form.kassa_id,
            comment=form.comment,
        )
        save_in_db(db, new_income_db)
        db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
            Kassas.balance: Kassas.balance + form.money
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source error!")


def update_income_e(form, db, thisuser):
    allowed_time = timedelta(minutes=5)
    if get_in_db(db, Incomes, form.id).time + allowed_time < datetime.now():
        raise HTTPException(status_code=400, detail="Time is already up!")
    get_in_db(db, Currencies, form.currency_id), get_in_db(db, Kassas, form.kassa_id)
    if db.query(Kassas).filter(Kassas.currency_id == form.currency_id).first() is None:
        raise HTTPException(status_code=400, detail="Current currency_id != Kassas.currency_id")
    if get_in_db(db, Customers, form.source_id) and form.source == "customer":
        old_money = get_in_db(db, Incomes, form.id).money
        db.query(Incomes).filter(Incomes.id == form.id).update({
            Incomes.money: form.money,
            Incomes.currency_id: form.currency_id,
            Incomes.source: form.source,
            Incomes.source_id: form.source_id,
            Incomes.kassa_id: form.kassa_id,
            Incomes.comment: form.comment
        })
        db.commit()
        new_money = get_in_db(db, Incomes, form.id).money
        db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
            Kassas.balance: Kassas.balance - old_money + new_money
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source error!")


def delete_income_e(id, db):
    allowed_time = timedelta(minutes=5)
    if get_in_db(db, Incomes, id).time + allowed_time < datetime.now():
        raise HTTPException(status_code=400, detail="Time is already up!")
    get_in_db(db, Incomes, id)
    db.query(Incomes).filter(Incomes.id == id).delete()
    db.commit()







