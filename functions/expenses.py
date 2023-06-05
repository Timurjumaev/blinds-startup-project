from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.currencies import Currencies
from models.customers import Customers
from models.kassas import Kassas
from models.suppliers import Suppliers
from models.users import Users
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.expenses import Expenses


def all_expenses(search, page, limit, kassa_id, db):
    expenses = db.query(Expenses).options(joinedload(Expenses.kassa),
                                          joinedload(Expenses.user),
                                          joinedload(Expenses.currency),
                                          joinedload(Expenses.source_user),
                                          joinedload(Expenses.source_supplier))
    search_format = "%{}%".format(search)
    search_filter = (Users.name.like(search_format)) | \
                    (Users.username.like(search_format)) | \
                    (Currencies.currency.like(search_format)) | \
                    (Kassas.name.like(search_format)) | \
                    (Suppliers.name.like(search_format))
    if search and kassa_id:
        expenses = expenses.filter(search_filter, Expenses.kassa_id == kassa_id).order_by(Expenses.id.asc())
    elif search is None and kassa_id:
        expenses = expenses.filter(Expenses.kassa_id == kassa_id).order_by(Expenses.id.asc())
    elif kassa_id is None and search:
        expenses = expenses.filter(search_filter).order_by(Expenses.id.asc())
    else:
        expenses = expenses.order_by(Expenses.id.asc())
    return pagination(expenses, page, limit)


def create_expense_e(form, db, thisuser):
    get_in_db(db, Currencies, form.currency_id), get_in_db(db, Kassas, form.kassa_id)
    if db.query(Kassas).filter(Kassas.currency_id == form.currency_id).first() is None:
        raise HTTPException(status_code=400, detail="Current currency_id != Kassas.currency_id")
    if (db.query(Suppliers).filter(Suppliers.id == form.source_id).first() and form.source == "supplier") or \
            (db.query(Users).filter(Users.id == form.source_id).first() and form.source == "user") or \
            (form.source_id == 0 and form.source == "others"):
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







