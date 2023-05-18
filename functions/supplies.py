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


def all_supplies(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Materials.name.like(search_formatted)) | \
                        (Suppliers.name.like(search_formatted)) | \
                        (Mechanisms.name.like(search_formatted)) | \
                        (Currencies.currency.like(search_formatted))
    else:
        search_filter = Supplies.id > 0
    supplies = db.query(Supplies).join(Supplies.material).join(Supplies.supplier).join(Supplies.mechanism).join(Supplies.currency)\
        .options(joinedload(Supplies.material), joinedload(Supplies.supplier), joinedload(Supplies.mechanism), joinedload(Supplies.currency))\
        .filter(search_filter).order_by(Supplies.id.asc())
    return pagination(supplies, page, limit)


def create_supply_y(form, db, thisuser):
    if get_in_db(db, Materials, form.material_id) and get_in_db(db, Mechanisms, form.mechanism_id) and \
            get_in_db(db, Suppliers, form.supplier_id) and get_in_db(db, Currencies, form.currency_id):
        new_supply_db = Supplies(
            material_id=form.material_id,
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
    supplier_balance = db.query(Supplier_balances).filter(Supplier_balances.supplier_id == form.supplier_id, Supplier_balances.currency_id == form.currency_id).first()
    if supplier_balance:
        db.query(Supplier_balances).filter(Supplier_balances.id == supplier_balance.id).update({
            Supplier_balances.balance: supplier_balance.balance - (form.price*form.quantity),
            Supplier_balances.currency_id: form.currency_id,
            Supplier_balances.supplier_id: form.supplier_id
        })
        db.commit()
    else:
        new_supplier_balance_db = Supplier_balances(
            balance=-(form.price * form.quantity),
            currency_id=form.currency_id,
            supplier_id=form.supplier_id
        )
        save_in_db(db, new_supplier_balance_db)





def update_supply_y(form, db, thisuser):
    supply_verification = db.query(Supplies).filter(Supplies.id == form.id, Supplies.status==False).first()
    if supply_verification is None:
        raise HTTPException(status_code=400, detail="Supply not found or this supply already added to warehouse materials!")
    if get_in_db(db, Materials, form.material_id) and\
            get_in_db(db, Mechanisms, form.mechanism_id) and get_in_db(db, Suppliers, form.supplier_id) and\
            get_in_db(db, Currencies, form.currency_id):
        supplier_filter = db.query(Supplier_balances).filter(Supplier_balances.supplier_id == form.supplier_id,
                                                             Supplier_balances.currency_id == form.currency_id)
        supplier_balance = supplier_filter.first()
        supplier_filter.update({
            Supplier_balances.balance: supplier_balance.balance + (supply_verification.price * supply_verification.quantity),
        })
        db.commit()
        supplier_filter.update({
            Supplier_balances.balance: supplier_balance.balance - (form.price * form.quantity),
        })
        db.commit()
        if form.status == False:
            user_id2 = 0
        else:
            if get_in_db(db, Warehouses, form.warehouse_id) and get_in_db(db, Cells, form.cell_id):
                user_id2 = thisuser.id
                new_warehouse_materials_db = Warehouse_materials(
                    material_id=form.material_id,
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