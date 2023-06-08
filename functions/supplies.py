from datetime import datetime
from fastapi import HTTPException
from models.cells import Cells
from models.supplier_balances import Supplier_balances
from models.warehouse_materials import Warehouse_materials
from models.supplies import Supplies
from models.materials import Materials
from models.mechanisms import Mechanisms
from models.suppliers import Suppliers
from models.currencies import Currencies
from models.warehouses import Warehouses
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from sqlalchemy.orm import joinedload


def all_supplies(search, page, limit, supplier_id, status, db):
    supplies = db.query(Supplies).options(joinedload(Supplies.material), joinedload(Supplies.supplier),
                                          joinedload(Supplies.mechanism), joinedload(Supplies.currency))
    if status:
        status_filter = Supplies.status == True
    elif status is False:
        status_filter = Supplies.status == False
    else:
        status_filter = Supplies.id > 0
    if search and supplier_id:
        search_formatted = "%{}%".format(search)
        supplies = supplies.filter(Materials.name.like(search_formatted) |
                                   Suppliers.name.like(search_formatted) |
                                   Mechanisms.name.like(search_formatted) |
                                   Currencies.currency.like(search_formatted))
        supplies = supplies.filter(Supplies.supplier_id == supplier_id, status_filter).order_by(Supplies.id.asc())
    elif search is None and supplier_id:
        supplies = supplies.filter(Supplies.supplier_id == supplier_id, status_filter).order_by(Supplies.id.asc())
    elif supplier_id is None and search:
        search_formatted = "%{}%".format(search)
        supplies = supplies.filter(Materials.name.like(search_formatted) |
                                   Suppliers.name.like(search_formatted) |
                                   Mechanisms.name.like(search_formatted) |
                                   Currencies.currency.like(search_formatted))
        supplies = supplies.filter(status_filter).order_by(Supplies.id.asc())
    else:
        supplies = supplies.filter(status_filter).order_by(Supplies.id.asc())
    return pagination(supplies, page, limit)


def create_supply_y(form, db, thisuser):
    if get_in_db(db, Suppliers, form.supplier_id) and get_in_db(db, Currencies, form.currency_id):
        if (db.query(Materials).filter(Materials.id == form.material_id).first() and form.mechanism_id == 0) or \
                (db.query(Mechanisms).filter(Mechanisms.id == form.mechanism_id).first() and form.material_id == 0):
            new_supply_db = Supplies(
                material_id=form.material_id,
                width=form.width,
                height=form.height,
                mechanism_id=form.mechanism_id,
                quantity=form.quantity,
                price=form.price,
                currency_id=form.currency_id,
                supplier_id=form.supplier_id,
                cr_time=datetime.now(),
                up_time=0,
                user_id1=thisuser.id,
                status=False,
                user_id2=0
            )
            save_in_db(db, new_supply_db)
        else:
            raise HTTPException(status_code=400, detail="You must input material or mechanism!")
    supplier_balance = db.query(Supplier_balances).filter(Supplier_balances.supplier_id == form.supplier_id, Supplier_balances.currency_id == form.currency_id).first()
    if supplier_balance and db.query(Mechanisms).filter(Mechanisms.id == form.mechanism_id).first():
        db.query(Supplier_balances).filter(Supplier_balances.id == supplier_balance.id).update({
            Supplier_balances.balance: supplier_balance.balance + (form.price*form.quantity),
        })
        db.commit()
    elif supplier_balance and db.query(Materials).filter(Materials.id == form.material_id).first():
        db.query(Supplier_balances).filter(Supplier_balances.id == supplier_balance.id).update({
            Supplier_balances.balance: supplier_balance.balance + (form.price * form.width * form.height),
        })
        db.commit()
    elif supplier_balance is None and db.query(Materials).filter(Materials.id == form.material_id).first():
        new_supplier_balance_db = Supplier_balances(
            balance=form.price * form.width * form.height,
            currency_id=form.currency_id,
            supplier_id=form.supplier_id
        )
        save_in_db(db, new_supplier_balance_db)
    elif supplier_balance is None and db.query(Mechanisms).filter(Mechanisms.id == form.mechanism_id).first():
        new_supplier_balance_db = Supplier_balances(
            balance=form.price * form.quantity,
            currency_id=form.currency_id,
            supplier_id=form.supplier_id
        )
        save_in_db(db, new_supplier_balance_db)


def update_supply_y(form, db, thisuser):
    supply_verification = db.query(Supplies).filter(Supplies.id == form.id, Supplies.status == False).first()
    material = db.query(Materials).filter(Materials.id == form.material_id).first()
    mechanism = db.query(Mechanisms).filter(Mechanisms.id == form.mechanism_id).first()
    if supply_verification is None:
        raise HTTPException(status_code=400, detail="Supply not found or this supply already added to warehouse materials!")
    get_in_db(db, Suppliers, form.supplier_id), get_in_db(db, Currencies, form.currency_id)
    if (material and mechanism) or (form.mechanism_id == 0 and form.material_id == 0):
        raise HTTPException(status_code=400, detail="You may input only Material or only Mechanism")
    supplier_filter = db.query(Supplier_balances).filter(Supplier_balances.supplier_id == form.supplier_id,
                                                         Supplier_balances.currency_id == form.currency_id)
    if material:
        supplier_balance = supplier_filter.first()
        supplier_filter.update({
            Supplier_balances.balance: supplier_balance.balance - (
                    supply_verification.width * supply_verification.height * supply_verification.price),
        })
        db.commit()
        supplier_filter.update({
            Supplier_balances.balance: supplier_balance.balance + (form.width * form.height * form.price),
        })
        db.commit()
    elif mechanism:
        supplier_balance = supplier_filter.first()
        supplier_filter.update({
            Supplier_balances.balance: supplier_balance.balance - (
                    supply_verification.quantity * supply_verification.price),
        })
        db.commit()
        supplier_filter.update({
            Supplier_balances.balance: supplier_balance.balance + (form.quantity * form.price),
        })
        db.commit()

    if form.status == False:
        user_id2 = 0
    else:
        get_in_db(db, Warehouses, form.warehouse_id), get_in_db(db, Cells, form.cell_id)
        user_id2 = thisuser.id
        new_warehouse_materials_db = Warehouse_materials(
            material_id=form.material_id,
            width=form.width,
            height=form.height,
            mechanism_id=form.mechanism_id,
            quantity=form.quantity,
            price=form.price,
            currency_id=form.currency_id,
            warehouse_id=form.warehouse_id,
            cell_id=form.cell_id,
        )
        save_in_db(db, new_warehouse_materials_db)

    db.query(Supplies).filter(Supplies.id == form.id).update({
        Supplies.material_id: form.material_id,
        Supplies.width: form.width,
        Supplies.height: form.height,
        Supplies.mechanism_id: form.mechanism_id,
        Supplies.quantity: form.quantity,
        Supplies.price: form.price,
        Supplies.currency_id: form.currency_id,
        Supplies.supplier_id: form.supplier_id,
        Supplies.up_time: datetime.now(),
        Supplies.status: form.status,
        Supplies.user_id2: user_id2
    })
    db.commit()
