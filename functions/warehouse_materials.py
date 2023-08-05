from sqlalchemy.orm import joinedload
from models.cells import Cells
from models.collactions import Collactions
from models.currencies import Currencies
from models.materials import Materials
from models.mechanisms import Mechanisms
from models.warehouses import Warehouses
from utils.db_operations import the_one
from utils.pagination import pagination
from models.warehouse_materials import Warehouse_materials


def all_warehouse_materials(search, page, limit, cell_id, db, thisuser):
    wms = db.query(Warehouse_materials).filter(Warehouse_materials.branch_id == thisuser.branch_id).\
                                        options(joinedload(Warehouse_materials.material).options(joinedload(Materials.collaction).subqueryload(Collactions.category)),
                                                joinedload(Warehouse_materials.warehouse),
                                                joinedload(Warehouse_materials.mechanism).options(joinedload(Mechanisms.collaction).subqueryload(Collactions.category)),
                                                joinedload(Warehouse_materials.currency),
                                                joinedload(Warehouse_materials.cell))
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Materials.name.like(search_formatted)) | \
                        (Warehouses.name.like(search_formatted)) | \
                        (Mechanisms.name.like(search_formatted)) | \
                        (Currencies.currency.like(search_formatted))
    else:
        search_filter = Warehouse_materials.id > 0
    if cell_id:
        cell_filter = Warehouse_materials.cell_id == cell_id
    else:
        cell_filter = Warehouse_materials.id > 0
    wms = wms.filter(search_filter, cell_filter).order_by(Warehouse_materials.id.desc())
    return pagination(wms, page, limit)


def update_warehouse_materials_s(form, db, user):
    m = the_one(db, Warehouse_materials, form.id, user)
    the_one(db, Cells, form.cell_id, user)
    old_cell = db.query(Cells).filter(Cells.id == m.cell_id).first()
    db.query(Warehouse_materials).filter(Warehouse_materials.id == form.id).update({
        Warehouse_materials.cell_id: form.cell_id,
    })
    db.commit()
    if db.query(Warehouse_materials).filter(Warehouse_materials.cell_id == old_cell.id).first() is None:
        db.query(Cells).filter(Cells.id == old_cell.id).update({
            Cells.busy: False,
        })
        db.commit()
    db.query(Cells).filter(Cells.id == form.cell_id).update({
        Cells.busy: True
    })
    db.commit()

