from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.categories import Categories


def all_categories(search, page, limit, db):
    if search :
        search_formatted = "%{}%".format(search)
        search_filter = (Categories.name.like(search_formatted))
    else :
        search_filter = Categories.id > 0
    categories = db.query(Categories).filter(search_filter).order_by(Categories.name.asc())
    return pagination(categories, page, limit)


def create_category_y(form, db):
    new_category_db = Categories(
        name=form.name,
        width_norm=form.width_norm,
        height_norm=form.height_norm,
        width_max=form.width_max,
        height_max=form.height_max
    )
    save_in_db(db, new_category_db)


def update_category_y(form, db):
    if get_in_db(db, Categories, form.id):
        db.query(Categories).filter(Categories.id == form.id).update({
            Categories.name: form.name,
            Categories.width_norm: form.width_norm,
            Categories.height_norm: form.height_norm,
            Categories.width_max: form.width_max,
            Categories.height_max: form.height_max
        })
        db.commit()

