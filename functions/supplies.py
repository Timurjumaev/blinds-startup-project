from datetime import datetime
from fastapi import HTTPException
from models.cells import Cells
from models.collactions import Collactions
from models.supplier_balances import Supplier_balances
from models.warehouse_materials import Warehouse_materials
from models.supplies import Supplies
from models.materials import Materials
from models.mechanisms import Mechanisms
from models.suppliers import Suppliers
from models.currencies import Currencies
from models.warehouses import Warehouses
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from sqlalchemy.orm import joinedload


def all_supplies(search, page, limit, supplier_id, status, db, thisuser):
    supplies = db.query(Supplies).filter(Supplies.branch_id == thisuser.branch_id).options(joinedload(Supplies.material).options(joinedload(Materials.collaction).subqueryload(Collactions.category)),
                                                                                           joinedload(Supplies.supplier),
                                                                                           joinedload(Supplies.mechanism).options(joinedload(Mechanisms.collaction).subqueryload(Collactions.category)),
                                                                                           joinedload(Supplies.currency),
                                                                                           joinedload(Supplies.warehouse).load_only(Warehouses.name),
                                                                                           joinedload(Supplies.cell))
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
    the_one(db, Suppliers, form.supplier_id, thisuser), the_one(db, Currencies, form.currency_id, thisuser)
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
            user_id2=0,
            branch_id=thisuser.branch_id
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
            supplier_id=form.supplier_id,
            branch_id=thisuser.branch_id
        )
        save_in_db(db, new_supplier_balance_db)
    elif supplier_balance is None and db.query(Mechanisms).filter(Mechanisms.id == form.mechanism_id).first():
        new_supplier_balance_db = Supplier_balances(
            balance=form.price * form.quantity,
            currency_id=form.currency_id,
            supplier_id=form.supplier_id,
            branch_id=thisuser.branch_id

        )
        save_in_db(db, new_supplier_balance_db)


def update_supply_y(form, db, thisuser):
    supply_verification = db.query(Supplies).filter(Supplies.id == form.id, Supplies.status == False).first()
    material = db.query(Materials).filter(Materials.id == form.material_id).first()
    mechanism = db.query(Mechanisms).filter(Mechanisms.id == form.mechanism_id).first()
    if supply_verification is None:
        raise HTTPException(status_code=400, detail="Supply not found or this supply already added to warehouse materials!")
    the_one(db, Suppliers, form.supplier_id, thisuser), the_one(db, Currencies, form.currency_id, thisuser)
    if (material and mechanism) or (material is None and mechanism is None):
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
    if form.status:
        the_one(db, Warehouses, form.warehouse_id, thisuser), the_one(db, Cells, form.cell_id, thisuser)
        user_id2 = thisuser.id
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
            Supplies.user_id2: user_id2,
            Supplies.warehouse_id: form.warehouse_id,
            Supplies.cell_id: form.cell_id
        })
        db.query(Cells).filter(Cells.id == form.cell_id).update({
            Cells.busy: True
        })
        db.commit()
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
            branch_id=thisuser.branch_id
        )
        save_in_db(db, new_warehouse_materials_db)
    else:
        user_id2 = 0
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
