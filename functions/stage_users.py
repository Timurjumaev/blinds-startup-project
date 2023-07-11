from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from models.users import Users
from models.stage_users import Stage_users
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.stages import Stages


def all_stage_users(search, page, limit, stage_id, db, thisuser):
    stage_users = db.query(Stage_users).filter(Stage_users.branch_id == thisuser.branch_id)\
        .options(joinedload(Stage_users.stage), joinedload(Stage_users.user), joinedload(Stage_users.currency))
    if search and stage_id:
        search_formatted = "%{}%".format(search)
        stage_users = stage_users.filter(Stage_users.kpi.like(search_formatted) |
                                         Stages.name.like(search_formatted) |
                                         Stages.number.like(search_formatted) |
                                         Users.name.like(search_formatted) |
                                         Users.username.like(search_formatted))
        stage_users = stage_users.filter(Stage_users.stage_id == stage_id).order_by(Stage_users.id.asc())
    elif search is None and stage_id:
        stage_users = stage_users.filter(Stage_users.stage_id == stage_id).order_by(Stage_users.id.asc())
    elif stage_id is None and search:
        search_formatted = "%{}%".format(search)
        stage_users = stage_users.filter(Stage_users.kpi.like(search_formatted) |
                                         Stages.name.like(search_formatted) |
                                         Stages.number.like(search_formatted) |
                                         Users.name.like(search_formatted) |
                                         Users.username.like(search_formatted))
        stage_users = stage_users.order_by(Stage_users.id.asc())
    else:
        stage_users = stage_users.order_by(Stage_users.id.asc())
    return pagination(stage_users, page, limit)


def create_stage_users_s(form, db, thisuser):
    the_one(db, Users, form.user_id, thisuser), the_one(db, Stages, form.stage_id, thisuser), \
        the_one(db, Currencies, form.currency_id, thisuser)
    new_stage_users_db = Stage_users(
        user_id=form.user_id,
        kpi=form.kpi,
        currency_id=form.currency_id,
        stage_id=form.stage_id,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_stage_users_db)


def update_stage_users_s(form, db, user):
    the_one(db, Stage_users, form.id, user), the_one(db, Users, form.user_id, user), \
        the_one(db, Stages, form.stage_id, user), the_one(db, Currencies, form.currency_id, user)
    db.query(Stage_users).filter(Stage_users.id == form.id).update({
        Stage_users.user_id: form.user_id,
        Stage_users.kpi: form.kpi,
        Stage_users.currency_id: form.currency_id,
        Stage_users.stage_id: form.stage_id,
    })
    db.commit()


def delete_stage_user_r(id, db, user):
    the_one(db, Stage_users, id, user)
    db.query(Stage_users).filter(Stage_users.id == id).delete()
    db.commit()
