from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.notifications import manager
from models.currencies import Currencies
from models.kassas import Kassas
from models.supplier_balances import Supplier_balances
from models.suppliers import Suppliers
from models.user_balances import User_balances
from models.users import Users
from schemas.notifications import NotificationSchema
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.expenses import Expenses


def all_expenses(search, page, limit, kassa_id, db, thisuser):
    allowed_time = timedelta(minutes=5)
    for expense in db.query(Expenses).filter(Expenses.branch_id == thisuser.branch_id).all():
        if expense.time + allowed_time < datetime.now():
            db.query(Expenses).filter(Expenses.id == expense.id).update({
                Expenses.updelstatus: False
            })
            db.commit()
    expenses = db.query(Expenses).filter(Expenses.branch_id == thisuser.branch_id).\
        options(joinedload(Expenses.kassa),
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


async def create_expense_e(form, db, thisuser):
    the_one(db, Currencies, form.currency_id, thisuser), the_one(db, Kassas, form.kassa_id, thisuser)
    users = db.query(Users).filter(Users.status, Users.branch_id == thisuser.branch_id, Users.role == "admin").all()
    this_kassa = db.query(Kassas).filter(Kassas.id == form.kassa_id, Kassas.currency_id == form.currency_id).first()
    if this_kassa is None:
        raise HTTPException(status_code=400, detail="Expencega kiritilayotgan currency bilan expence olinayotgan kassaning currencysi bir xil emas!")
    if this_kassa.balance < form.money:
        raise HTTPException(status_code=400, detail="Kassada yetarli mablag' mavjud emas!")
    if db.query(Suppliers).filter(Suppliers.id == form.source_id).first() \
            and form.source == "supplier" and form.money > 0:
        new_expense_db = Expenses(
            money=form.money,
            currency_id=form.currency_id,
            source=form.source,
            source_id=form.source_id,
            time=datetime.now(),
            user_id=thisuser.id,
            kassa_id=form.kassa_id,
            comment=form.comment,
            updelstatus=True,
            branch_id=thisuser.branch_id,
        )
        save_in_db(db, new_expense_db)
        this_currency = db.query(Currencies).filter(Currencies.id == form.currency_id).first()
        for user in users:
            data = NotificationSchema(
                title="Yangi chiqim!",
                body=f"Hurmatli foydalanuvchi {form.money} {this_currency.currency} miqdorda chiqim bo'ldi!",
                user_id=user.id,
            )
            await manager.send_user(message=data, user_id=user.id, db=db)
        db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
            Kassas.balance: Kassas.balance - form.money
        })
        db.commit()
        supplier_balance = db.query(Supplier_balances).filter(Supplier_balances.supplier_id == form.source_id,
                                                              Supplier_balances.currency_id == form.currency_id)
        if supplier_balance.first():
            supplier_balance.update({
                Supplier_balances.balance: Supplier_balances.balance - form.money
            })
        else:
            new_supplier_balance = Supplier_balances(
                balance=-form.money,
                currency_id=form.currency_id,
                supplier_id=form.source_id,
                branch_id=thisuser.branch_id
            )
            save_in_db(db, new_supplier_balance)
    elif (db.query(Users).filter(Users.id == form.source_id).first() and form.source == "user" and form.money > 0)\
            or (form.source_id == 0 and form.source == "others" and form.money > 0):
        new_expense_db = Expenses(
            money=form.money,
            currency_id=form.currency_id,
            source=form.source,
            source_id=form.source_id,
            time=datetime.now(),
            user_id=thisuser.id,
            kassa_id=form.kassa_id,
            comment=form.comment,
            updelstatus=True,
            branch_id=thisuser.branch_id
        )
        save_in_db(db, new_expense_db)
        this_currency = db.query(Currencies).filter(Currencies.id == form.currency_id).first()
        for user in users:
            data = NotificationSchema(
                title="Yangi chiqim!",
                body=f"Hurmatli foydalanuvchi {form.money} {this_currency.currency} miqdorda chiqim bo'ldi!",
                user_id=user.id,
            )
            await manager.send_user(message=data, user_id=user.id, db=db)
        db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
            Kassas.balance: Kassas.balance - form.money
        })
        db.commit()
        user_balance = db.query(User_balances).filter(User_balances.user_id == form.source_id,
                                                      User_balances.currency_id == form.currency_id)
        if user_balance.first():
            user_balance.update({
                User_balances.balance: User_balances.balance - form.money
            })
        else:
            new_user_balance = User_balances(
                balance=-form.money,
                currency_id=form.currency_id,
                user_id=form.source_id,
                branch_id=thisuser.branch_id
            )
            save_in_db(db, new_user_balance)
    else:
        raise HTTPException(status_code=400, detail="source error or money <=0")


def delete_expense_e(id, db, user):
    allowed_time = timedelta(minutes=5)
    this_expense = the_one(db, Expenses, id, user)
    if this_expense.time + allowed_time < datetime.now():
        raise HTTPException(status_code=400, detail="Time is already up!")
    db.query(Expenses).filter(Expenses.id == id).delete()
    db.query(Kassas).filter(Kassas.id == this_expense.kassa_id).update({
        Kassas.balance: Kassas.balance + this_expense.money
    })
    if this_expense.source == "user":
        db.query(User_balances).filter(User_balances.user_id == this_expense.source_id,
                                       User_balances.currency_id == this_expense.currency_id).update({
            User_balances.balance: User_balances.balance + this_expense.money
        })
    elif this_expense.source == "supplier":
        db.query(Supplier_balances).filter(Suppliers.id == this_expense.source_id,
                                           Supplier_balances.currency_id == this_expense.currency_id).update({
            Supplier_balances.balance: Supplier_balances.balance + this_expense.money
        })
    db.commit()








