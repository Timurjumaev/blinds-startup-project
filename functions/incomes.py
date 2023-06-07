from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.currencies import Currencies
from models.kassas import Kassas
from models.loans import Loans
from models.orders import Orders
from models.users import Users
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.incomes import Incomes


def all_incomes(search, page, limit, kassa_id, db):
    allowed_time = timedelta(minutes=5)
    for expense in db.query(Incomes).all():
        if expense.time + allowed_time < datetime.now():
            db.query(Incomes).filter(Incomes.id == expense.id).update({
                Incomes.updelstatus: False
            })
            db.commit()
    incomes = db.query(Incomes).options(joinedload(Incomes.kassa),
                                        joinedload(Incomes.user),
                                        joinedload(Incomes.currency),
                                        joinedload(Incomes.source_order),
                                        joinedload(Incomes.source_loan))
    search_format = "%{}%".format(search)
    search_filter = (Users.name.like(search_format)) | \
                    (Users.username.like(search_format)) | \
                    (Currencies.currency.like(search_format)) | \
                    (Kassas.name.like(search_format))
    if search and kassa_id:
        incomes = incomes.filter(search_filter, Incomes.kassa_id == kassa_id).order_by(Incomes.id.asc())
    elif search is None and kassa_id:
        incomes = incomes.filter(Incomes.kassa_id == kassa_id).order_by(Incomes.id.asc())
    elif kassa_id is None and search:
        incomes = incomes.filter(search_filter).order_by(Incomes.id.asc())
    else:
        incomes = incomes.order_by(Incomes.id.asc())
    return pagination(incomes, page, limit)


def create_income_e(form, db, thisuser):
    get_in_db(db, Currencies, form.currency_id), get_in_db(db, Kassas, form.kassa_id)
    if db.query(Kassas).filter(Kassas.currency_id == form.currency_id).first() is None:
        raise HTTPException(status_code=400, detail="Current currency_id != Kassas.currency_id")
    if (db.query(Orders).filter(Orders.id == form.source_id).first() and form.source == "order") or \
            (db.query(Loans).filter(Loans.id == form.source_id).first() and form.source == "loan"):
        new_income_db = Incomes(
            money=form.money,
            currency_id=form.currency_id,
            source=form.source,
            source_id=form.source_id,
            time=datetime.now(),
            user_id=thisuser.id,
            kassa_id=form.kassa_id,
            comment=form.comment,
            updelstatus=True
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
    if (db.query(Orders).filter(Orders.id == form.source_id).first() and form.source == "order") or \
            (db.query(Loans).filter(Loans.id == form.source_id).first() and form.source == "loan"):
        old_money = get_in_db(db, Incomes, form.id).money
        db.query(Incomes).filter(Incomes.id == form.id).update({
            Incomes.money: form.money,
            Incomes.currency_id: form.currency_id,
            Incomes.source: form.source,
            Incomes.source_id: form.source_id,
            Incomes.user_id: thisuser.id,
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







