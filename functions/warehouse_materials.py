from models.cells import Cells
from utils.db_operations import get_in_db
from utils.pagination import pagination
from models.warehouse_materials import Warehouse_materials


def all_warehouse_materials(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Warehouse_materials.price.like(search_formatted))
    else:
        search_filter = Warehouse_materials.id > 0
    warehouse_materials = db.query(Warehouse_materials).filter(search_filter).order_by(Warehouse_materials.price.asc())
    return pagination(warehouse_materials, page, limit)


def update_warehouse_materials_s(form, db):
    if get_in_db(db, Warehouse_materials, form.id) and get_in_db(db, Cells, form.cell_id):
        db.query(Warehouse_materials).filter(Warehouse_materials.id == form.id).update({
            Warehouse_materials.cell_id: form.cell_id,
        })
        db.commit()