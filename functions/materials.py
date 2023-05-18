from models.collactions import Collactions
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.materials import Materials


def all_materials(search, page, limit, col_id, db):
    materials = db.query(Materials)
    if search:
        search_formatted = "%{}%".format(search)
        materials = materials.filter(Materials.name.like(search_formatted))
    if col_id:
        materials = materials.filter(Materials.collaction_id == col_id)
    materials = materials.order_by(Materials.name.asc())
    return pagination(materials, page, limit)


def create_material_l(form, db):
    if get_in_db(db, Collactions, form.collaction_id):
        new_material_db = Materials(
            name=form.name,
            comment=form.comment,
            collaction_id=form.collaction_id
        )
        save_in_db(db, new_material_db)


def update_material_l(form, db):
    if get_in_db(db, Materials, form.id) and get_in_db(db, Collactions, form.collaction_id):
        db.query(Materials).filter(Materials.id == form.id).update({
            Materials.name: form.name,
            Materials.comment: form.comment,
            Materials.collaction_id: form.collaction_id
        })
        db.commit()

