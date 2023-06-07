from sqlalchemy.orm import joinedload
from models.currencies import Currencies
from models.loans import Loans
from models.orders import Orders
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination


def all_loans(search, page, limit, order_id, db):
    loans = db.query(Loans).options(joinedload(Loans.order))
    search_formatted = "%{}%".format(search)
    search_filter = Loans.money.like(search_formatted) | \
                    Loans.residual.like(search_formatted) | \
                    Loans.comment.like(search_formatted)
    if search and order_id:
        loans = loans.filter(search_filter, Loans.order_id == order_id).order_by(Loans.id.asc())
    elif search is None and order_id:
        loans = loans.filter(Loans.order_id == order_id).order_by(Loans.id.asc())
    elif order_id is None and search:
        loans = loans.filter(search_filter).order_by(Loans.id.asc())
    else:
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
