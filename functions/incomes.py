from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.collactions import Collactions
from models.currencies import Currencies
from models.customers import Customers
from models.discounts import Discounts
from models.kassas import Kassas
from models.loans import Loans
from models.materials import Materials
from models.orders import Orders
from models.prices import Prices
from models.trades import Trades
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
    if form.currency_id != get_in_db(db, Kassas, form.kassa_id).currency_id:
        raise HTTPException(status_code=400, detail="Incomega kiritilayotgan currency bilan income kiritilayotgan kassaning currencysi bir xil emas!")
    thisorder = db.query(Orders).filter(Orders.id == form.source_id).first()
    thisloan = db.query(Loans).filter(Loans.id == form.source_id).first()
    if thisorder and form.source == "order":
        this_order = get_in_db(db, Orders, form.source_id)
        money = 0
        trades = db.query(Trades).filter(Trades.order_id == form.source_id).all()
        for trade in trades:
            material = db.query(Materials).filter(Materials.id == trade.material_id).first()
            collaction = db.query(Collactions).filter(Collactions.id == material.collaction_id).first()
            price = db.query(Prices).filter(Prices.collaction_id == collaction.id,
                                            Prices.width1 <= trade.width,
                                            Prices.width2 >= trade.width,
                                            Prices.height1 <= trade.height,
                                            Prices.height2 >= trade.height).first()
            if price:
                this_money = price.price
                this_currency = db.query(Currencies).filter(Currencies.id == price.currency_id).first()
                this_money = this_money * this_currency.price
                money = money + this_money
            else:
                raise HTTPException(status_code=400,
                                    detail="Ushbu o'lchamdagi material tegishli bo'lgan kolleksiyaga hali narx belgilanmagan!")
        this_customer = db.query(Customers).filter(Customers.id == this_order.customer_id).first()
        this_discount = db.query(Discounts).filter(Discounts.type == this_customer.type).first()
        if this_discount is None:
            raise HTTPException(status_code=400, detail="Mijozni typega teng bolgan typeli discount topilmadi!")
        total_discount = (money * this_discount.percent) / 100
        total_money = money - total_discount
        income_currency = db.query(Currencies).filter(Currencies.id == form.currency_id).first()
        total_money_income_currency = total_money / income_currency.price
        if total_money_income_currency < form.money or total_money_income_currency <= 0 or \
                db.query(Incomes).filter(Incomes.source_id == form.source_id, Incomes.source == "order").first():
            raise HTTPException(status_code=400,
                                detail="Kiritilayotgan summa ushbu buyurtmaning narxidan katta yoki manfiy yoki"
                                       "ushbu buyurtmaga tegishli income allaqachon mavjud!")
        elif total_money_income_currency > form.money:
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
            new_loan_db = Loans(
                money=total_money_income_currency - form.money,
                currency_id=form.currency_id,
                residual=total_money_income_currency - form.money,
                order_id=form.source_id,
                return_date=0,
                comment=0,
                status=False
            )
            save_in_db(db, new_loan_db)
        elif total_money_income_currency == form.money:
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
    elif thisloan and form.source == "loan":
        if thisloan.residual < form.money or form.money <= 0:
            raise HTTPException(status_code=400, detail="Kiritilayotgan pul miqdori nasiya qoldigidan kop yoki manfiy!")
        elif thisloan.residual > form.money:
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
            db.query(Loans).filter(Loans.id == thisloan.id).update({
                Loans.residual: Loans.residual - form.money
            })
            db.commit()
            db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
                Kassas.balance: Kassas.balance + form.money
            })
            db.commit()
        elif thisloan.residual == form.money:
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
            db.query(Loans).filter(Loans.id == thisloan.id).update({
                Loans.residual: Loans.residual - form.money,
                Loans.status: True
            })
            db.commit()
            db.query(Kassas).filter(Kassas.id == form.kassa_id).update({
                Kassas.balance: Kassas.balance + form.money
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







