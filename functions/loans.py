from sqlalchemy import func
from sqlalchemy.orm import joinedload
from functions.orders import one_order_r
from models.incomes import Incomes
from models.loans import Loans
from models.orders import Orders
from utils.db_operations import the_one, save_in_db
from utils.pagination import pagination
from fastapi import HTTPException


def all_loans(search, page, limit, order_id, arxiv, db, thisuser):
    loans = db.query(Loans).filter(Loans.branch_id == thisuser.branch_id).options(joinedload(Loans.order),
                                                                                  joinedload(Loans.currency))
    if arxiv:
        arxiv_filter = Loans.residual == 0
    else:
        arxiv_filter = Loans.residual != 0
    search_formatted = "%{}%".format(search)
    search_filter = Loans.comment.like(search_formatted)
    if search and order_id:
        loans = loans.filter(search_filter, Loans.order_id == order_id, arxiv_filter).order_by(Loans.id.asc())
    elif search is None and order_id:
        loans = loans.filter(Loans.order_id == order_id, arxiv_filter).order_by(Loans.id.asc())
    elif order_id is None and search:
        loans = loans.filter(search_filter, arxiv_filter).order_by(Loans.id.asc())
    else:
        loans = loans.filter(arxiv_filter).order_by(Loans.id.asc())
    return pagination(loans, page, limit)


# def create_loan_n(form, db, user):
#     order = the_one(db, Orders, form.order_id, user)
#     income = db.query(Incomes).filter(Incomes.source == "order").first()
#     if order.status != "done":
#         raise HTTPException(status_code=400, detail="Tanlangan buyurtma hali yakunlanmagan!")
#     incomes = db.query(Incomes, func.sum(Incomes.money).label("total_sum"))\
#         .filter(Incomes.source == "order", Incomes.source_id == form.order_id).all()
#     order_money = one_order_r(form.order_id, db, user)
#     if order_money.money > incomes.total_sum:
#         loan = Loans(
#             money=order_money.money - incomes.total_sum,
#             currency_id=income.currency_id,
#             residual=order_money.money - incomes.total_sum,
#             order_id=form.order_id,
#             return_date=form.return_date,
#             comment=form.comment,
#             status=False,
#             branch_id=user.branch_id
#         )
#         save_in_db(db, loan)


def update_loan_n(form, db, user):
    the_one(db, Loans, form.id, user)
    db.query(Loans).filter(Loans.id == form.id).update({
        Loans.return_date: form.return_date,
        Loans.comment: form.comment,
    })
    db.commit()

