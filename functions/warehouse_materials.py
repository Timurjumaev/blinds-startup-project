from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from models.cells import Cells
from models.currencies import Currencies
from models.materials import Materials
from models.mechanisms import Mechanisms
from models.warehouses import Warehouses
from utils.db_operations import get_in_db
from utils.pagination import pagination
from models.warehouse_materials import Warehouse_materials


def all_warehouse_materials(search, page, limit, inspection, db):
    wms = db.query(Warehouse_materials).options(joinedload(Warehouse_materials.material),
                                                joinedload(Warehouse_materials.warehouse),
                                                joinedload(Warehouse_materials.mechanism),
                                                joinedload(Warehouse_materials.currency),
                                                joinedload(Warehouse_materials.cell))
    search_formatted = "%{}%".format(search)
    search_filter = (Materials.name.like(search_formatted)) | \
                    (Warehouses.name.like(search_formatted)) | \
                    (Mechanisms.name.like(search_formatted)) | \
                    (Currencies.currency.like(search_formatted))
    if inspection and inspection != "material" and inspection != "mechanism":
        raise HTTPException(status_code=400, detail="You may choose material or mechanism!")
    if inspection is None and search is None:
        wms = wms.order_by(Warehouse_materials.id.asc())
    elif inspection and search:
        wms = wms.filter(search_filter).order_by(Warehouse_materials.id.asc())
    elif inspection == "material" and search is None:
        wms = wms.filter(Warehouse_materials.mechanism_id == 0)\
            .order_by(Warehouse_materials.id.asc())
    elif inspection == "material" and search:
        wms = wms.filter(search_filter, Warehouse_materials.mechanism_id == 0) \
            .order_by(Warehouse_materials.id.asc())
    elif inspection == "mechanism" and search is None:
        wms = wms.filter(Warehouse_materials.material_id == 0) \
            .order_by(Warehouse_materials.id.asc())
    elif inspection == "material" and search:
        wms = wms.filter(search_filter, Warehouse_materials.material_id == 0) \
            .order_by(Warehouse_materials.id.asc())
    else:
        raise HTTPException(status_code=400, detail="Error on search!")
    return pagination(wms, page, limit)


def update_warehouse_materials_s(form, db):
    get_in_db(db, Warehouse_materials, form.id), get_in_db(db, Cells, form.cell_id)
    db.query(Warehouse_materials).filter(Warehouse_materials.id == form.id).update({
        Warehouse_materials.cell_id: form.cell_id,
    })
    db.commit()
