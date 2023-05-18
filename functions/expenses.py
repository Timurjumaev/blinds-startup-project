from datetime import datetime, timedelta

from fastapi import HTTPException

from models.currencies import Currencies
from models.customers import Customers
from models.kassas import Kassas
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.expenses import Expenses


def all_expenses(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Expenses.money.like(search_formatted))
    else:
        search_filter = Expenses.id > 0
    expenses = db.query(Expenses).filter(search_filter).order_by(Expenses.money.asc())
    return pagination(expenses, page, limit)


def create_expense_e(form, db, thisuser):
    get_in_db(db, Currencies, form.currency_id), get_in_db(db, Kassas, form.kassa_id)
    if db.query(Kassas).filter(Kassas.currency_id == form.currency_id).first() is None:
        raise HTTPException(status_code=400, detail="Current currency_id != Kassas.currency_id")
    if get_in_db(db, Customers, form.source_id) and form.source == "customer":
        new_expense_db = Expenses(
            money=form.money,
            currency_id=form.currency_id,
            source=form.source,
            source_id=form.source_id,
            time=datetime.now(),
            user_id=thisuser.id,
            kassa_id=form.kassa_id,
            comment=form.comment,
        )
        save_in_db(db, new_expense_db)
        db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
            Kassas.balance: Kassas.balance - form.money
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source error!")


def update_expense_e(form, db, thisuser):
    allowed_time = timedelta(minutes=5)
    if get_in_db(db, Expenses, form.id).time + allowed_time < datetime.now():
        raise HTTPException(status_code=400, detail="Time is already up!")
    get_in_db(db, Currencies, form.currency_id), get_in_db(db, Kassas, form.kassa_id)
    if db.query(Kassas).filter(Kassas.currency_id == form.currency_id).first() is None:
        raise HTTPException(status_code=400, detail="Current currency_id != Kassas.currency_id")
    if get_in_db(db, Customers, form.source_id) and form.source == "customer":
        old_money = get_in_db(db, Expenses, form.id).money
        db.query(Expenses).filter(Expenses.id == form.id).update({
            Expenses.money: form.money,
            Expenses.currency_id: form.currency_id,
            Expenses.source: form.source,
            Expenses.source_id: form.source_id,
            Expenses.kassa_id: form.kassa_id,
            Expenses.comment: form.comment
        })
        db.commit()
        new_money = get_in_db(db, Expenses, form.id).money
        db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
            Kassas.balance: Kassas.balance + old_money - new_money
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source error!")


def delete_expense_e(id, db):
    allowed_time = timedelta(minutes=5)
    if get_in_db(db, Expenses, id).time + allowed_time < datetime.now():
        raise HTTPException(status_code=400, detail="Time is already up!")
    get_in_db(db, Expenses, id)
    db.query(Expenses).filter(Expenses.id == id).delete()
    db.commit()







