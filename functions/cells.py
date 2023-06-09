from sqlalchemy.orm import joinedload
from models.warehouses import Warehouses
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.cells import Cells


def all_cells(search, page, limit, warehouse_id, db, thisuser):
    cells = db.query(Cells).filter(Cells.branch_id == thisuser.branch_id).join(Cells.warehouse).options(joinedload(Cells.warehouse))
    if search and warehouse_id:
        search_formatted = "%{}%".format(search)
        cells = cells.filter(Cells.name1.like(search_formatted) | Cells.name2.like(search_formatted) | Warehouses.name.like(search_formatted))
        cells = cells.filter(Cells.warehouse_id == warehouse_id).order_by(Cells.id.asc())
    elif search is None and warehouse_id:
        cells = cells.filter(Cells.warehouse_id == warehouse_id).order_by(Cells.id.asc())
    elif warehouse_id is None and search:
        search_formatted = "%{}%".format(search)
        cells = cells.filter(Cells.name1.like(search_formatted) | Cells.name2.like(search_formatted) | Warehouses.name.like(search_formatted))
        cells = cells.order_by(Cells.id.asc())
    else:
        cells = cells.order_by(Cells.id.asc())
    return pagination(cells, page, limit)


def create_cell_l(form, db, thisuser):
    the_one(db, Warehouses, form.warehouse_id, thisuser)
    new_cell_db = Cells(
        name1=form.name1,
        name2=form.name2,
        warehouse_id=form.warehouse_id,
        branch_id=thisuser.branch_id
        )
    save_in_db(db, new_cell_db)


def update_cell_l(form, db, user):
    the_one(db, Cells, form.id, user), the_one(db, Warehouses, form.warehouse_id, user)
    db.query(Cells).filter(Cells.id == form.id).update({
        Cells.name1: form.name1,
        Cells.name2: form.name2,
        Cells.warehouse_id: form.warehouse_id,
    })
    db.commit()
