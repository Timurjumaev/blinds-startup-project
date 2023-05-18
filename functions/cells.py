from sqlalchemy.orm import joinedload

from models.warehouses import Warehouses
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.cells import Cells


def all_cells(search, page, limit, db):
    cells = db.query(Cells).join(Cells.warehouse).options(joinedload(Cells.warehouse))
    if search:
        search_formatted = "%{}%".format(search)
        cells = cells.filter(Cells.name1.like(search_formatted) | Cells.name2.like(search_formatted) | Warehouses.name.like(search_formatted))
    cells = cells.order_by(Cells.name1.asc())
    return pagination(cells, page, limit)


def create_cell_l(form, db):
    if get_in_db(db, Warehouses, form.warehouse_id):
        new_cell_db = Cells(
            name1=form.name1,
            name2=form.name2,
            warehouse_id=form.warehouse_id,
            )
        save_in_db(db, new_cell_db)


def update_cell_l(form, db):
    if get_in_db(db, Cells, form.id) and get_in_db(db, Warehouses, form.warehouse_id):
        db.query(Cells).filter(Cells.id == form.id).update({
            Cells.name1: form.name1,
            Cells.name2: form.name2,
            Cells.warehouse_id: form.warehouse_id,
        })
        db.commit()