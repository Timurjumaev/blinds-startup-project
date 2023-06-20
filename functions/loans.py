from sqlalchemy.orm import joinedload
from models.loans import Loans
from utils.db_operations import the_one
from utils.pagination import pagination


def all_loans(search, page, limit, order_id, db, thisuser):
    loans = db.query(Loans).filter(Loans.branch_id == thisuser.branch_id).options(joinedload(Loans.order),
                                                                                  joinedload(Loans.currency))
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


def update_loan_n(form, db, user):
    the_one(db, Loans, form.id, user)
    db.query(Loans).filter(Loans.id == form.id).update({
        Loans.return_date: form.return_date,
        Loans.comment: form.comment,
    })
    db.commit()

