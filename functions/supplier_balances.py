from utils.pagination import pagination
from models.supplier_balances import Supplier_balances


def all_supplier_balances(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Supplier_balances.balance.like(search_formatted))
    else:
        search_filter = Supplier_balances.id > 0
    supplier_balances = db.query(Supplier_balances).filter(search_filter).order_by(Supplier_balances.balance.asc())
    return pagination(supplier_balances, page, limit)