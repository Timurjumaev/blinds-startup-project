from sqlalchemy.orm import joinedload
from models.currencies import Currencies
from models.loans import Loans
from models.orders import Orders
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination


def all_loans(search, page, limit, db):
    loans = db.query(Loans).options(joinedload(Loans.order),)
    if search:
        search_formatted = "%{}%".format(search)
        loans = loans.filter(Orders.status.like(search_formatted))
    loans = loans.order_by(Loans.id.asc())
    return pagination(loans, page, limit)


def create_loan_n(form, db):
    get_in_db(db, Currencies, form.currency_id), get_in_db(db, Orders, form.order_id)
    new_loan_db = Loans(
        money=form.money,
        currency_id=form.currency_id,
        residual=form.money,
        order_id=form.order_id,
        return_date=form.return_date
    )
    save_in_db(db, new_loan_db)


def update_loan_n(form, db):
    get_in_db(db, Loans, form.id), get_in_db(db, Currencies, form.currency_id), get_in_db(db, Orders, form.order_id)
    db.query(Loans).filter(Loans.id == form.id).update({
        Loans.currency_id: form.currency_id,
        Loans.residual: form.residual,
        Loans.order_id: form.order_id,
        Loans.return_date: form.return_date,
        Loans.comment: form.comment,
    })
    db.commit()


def delete_loan_n(id, db):
    get_in_db(db, Loans, id)
    db.query(Loans).filter(Loans.id == id).delete()
    db.commit()
