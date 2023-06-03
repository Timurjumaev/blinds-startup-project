# from sqlalchemy.orm import joinedload
# from models.mechanisms import Mechanisms
# from models.trades import Trades
# from utils.db_operations import save_in_db, get_in_db
# from utils.pagination import pagination
# from models.trade_mechanisms import Trade_mechanisms
#
#
# # def all_trade_mechanisms(search, page, limit, db):
# #     trade_mechanism = db.query(Trade_mechanisms).options(joinedload(Trade_mechanisms.mechanism))
# #     if search:
# #         search_formatted = "%{}%".format(search)
# #         trade_mechanism = trade_mechanism.filter(Mechanisms.name.like(search_formatted))
# #     trade_mechanism = trade_mechanism.order_by(Trade_mechanisms.id.asc())
# #     return pagination(trade_mechanism, page, limit)
#
#
# def create_trade_mechanism_m(form, db):
#     get_in_db(db, Trades, form.trade_id)
#     new_trade_mechanism_db = Trade_mechanisms(
#         trade_id=form.trade_id,
#         mechanism_id=form.mechanism_id,
#         width=form.width,
#         quantity=form.quantity
#     )
#     save_in_db(db, new_trade_mechanism_db)
#
#
#
