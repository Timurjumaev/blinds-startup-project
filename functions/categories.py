from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.categories import Categories


def all_categories(search, page, limit, db, thisuser):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Categories.name.like(search_formatted))
    else:
        search_filter = Categories.id > 0
    branch_filter = Categories.branch_id == thisuser.branch_id
    categories = db.query(Categories).filter(search_filter, branch_filter).order_by(Categories.name.asc())
    return pagination(categories, page, limit)


def create_category_y(form, db, thisuser):
    new_category_db = Categories(
        name=form.name,
        width_norm=form.width_norm,
        height_norm=form.height_norm,
        width_max=form.width_max,
        height_max=form.height_max,
        branch_id=thisuser.branch_id,
    )
    save_in_db(db, new_category_db)


def update_category_y(form, db, user):
    the_one(db, Categories, form.id, user)
    db.query(Categories).filter(Categories.id == form.id).update({
        Categories.name: form.name,
        Categories.width_norm: form.width_norm,
        Categories.height_norm: form.height_norm,
        Categories.width_max: form.width_max,
        Categories.height_max: form.height_max
    })
    db.commit()

