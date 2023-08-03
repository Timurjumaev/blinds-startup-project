from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.notifications import manager
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
from schemas.notifications import NotificationSchema
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.incomes import Incomes


def all_incomes(search, page, limit, kassa_id, db, thisuser):
    allowed_time = timedelta(minutes=5)
    for expense in db.query(Incomes).filter(Incomes.branch_id == thisuser.branch_id)\
            .options(joinedload(Incomes.source_order).options(joinedload(Orders.customer))).all():
        if expense.time + allowed_time < datetime.now():
            db.query(Incomes).filter(Incomes.id == expense.id).update({
                Incomes.updelstatus: False
            })
            db.commit()
    incomes = db.query(Incomes).filter(Incomes.branch_id == thisuser.branch_id).options(joinedload(Incomes.kassa),
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


async def create_income_e(form, db, thisuser):
    kassa = the_one(db, Kassas, form.kassa_id, thisuser)
    users = db.query(Users).filter(Users.status, Users.branch_id == thisuser.branch_id, Users.role == "admin").all()
    currency = db.query(Currencies).filter(Currencies.id == kassa.currency_id).first()
    if currency.currency != "so'm":
        raise HTTPException(status_code=400, detail="Kirim qilinayotgan kassaning valyutasi so'm emas!")
    thisorder = db.query(Orders).filter(Orders.id == form.source_id).first()
    thisloan = db.query(Loans).filter(Loans.id == form.source_id).first()
    if thisorder and form.source == "order":
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
        total_money = money - thisorder.discount
        incomes = db.query(Incomes).filter(Incomes.source_id == form.source_id, Incomes.source == form.source).all()
        total_income = 0
        if incomes:
            for income in incomes:
                total_income = total_income + income.money
        if total_income > 0:
            total_money = total_money - total_income
        if total_money < form.money or form.money <= 0:
            raise HTTPException(status_code=400,
                                detail="Kiritilayotgan summa ushbu buyurtmaning qoldiq narxidan katta yoki manfiy")
        new_income_db = Incomes(
            money=form.money,
            currency_id=currency.id,
            source=form.source,
            source_id=form.source_id,
            time=datetime.now(),
            user_id=thisuser.id,
            kassa_id=form.kassa_id,
            comment=form.comment,
            updelstatus=True,
            branch_id=thisuser.branch_id
        )
        save_in_db(db, new_income_db)
        if total_money == form.money:
            db.query(Orders).filter(Orders.id == form.source_id).update({
                Orders.money_status: True
            })
            db.commit()
        for user in users:
            data = NotificationSchema(
                title="Yangi kirim!",
                body=f"Hurmatli foydalanuvchi {form.money} so'm miqdorda kirim bo'ldi!",
                user_id=user.id,
            )
            await manager.send_user(message=data, user_id=user.id, db=db)
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
                updelstatus=True,
                branch_id=thisuser.branch_id
            )
            save_in_db(db, new_income_db)
            this_currency = db.query(Currencies).filter(Currencies.id == form.currency_id).first()
            for user in users:
                data = NotificationSchema(
                    title="Yangi kirim!",
                    body=f"Hurmatli foydalanuvchi {form.money} {this_currency.currency} miqdorda kirim bo'ldi!",
                    user_id=user.id,
                )
                await manager.send_user(message=data, user_id=user.id, db=db)
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
                updelstatus=True,
                branch_id=thisuser.branch_id
            )
            save_in_db(db, new_income_db)
            this_currency = db.query(Currencies).filter(Currencies.id == form.currency_id).first()
            for user in users:
                data = NotificationSchema(
                    title="Yangi kirim!",
                    body=f"Hurmatli foydalanuvchi {form.money} {this_currency.currency} miqdorda kirim bo'ldi!",
                    user_id=user.id,
                )
                await manager.send_user(message=data, user_id=user.id, db=db)
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


def delete_income_e(id, db, user):
    allowed_time = timedelta(minutes=5)
    this_income = the_one(db, Incomes, id, user)
    if this_income.time + allowed_time < datetime.now():
        raise HTTPException(status_code=400, detail="Time is already up!")
    db.query(Incomes).filter(Incomes.id == id).delete()
    db.query(Kassas).filter(Kassas.id == this_income.kassa_id).update({
        Kassas.balance: Kassas.balance - this_income.money
    })
    db.query(Loans).filter(Loans.id == this_income.source_id).update({
        Loans.residual: Loans.residual + this_income.money
    })
    db.commit()







