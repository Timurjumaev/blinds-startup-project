from sqlalchemy.orm import joinedload

from models.users import Users
from models.stage_users import Stage_users
from utils.db_operations import save_in_db, get_in_db
from utils.pagination import pagination
from models.stages import Stages


def all_stage_users(search, page, limit, stage_id, db):
    stage_users = db.query(Stage_users).options(joinedload(Stage_users.stage), joinedload(Stage_users.user))
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


def create_stage_users_s(form, db):
    if get_in_db(db, Users, form.user_id) and get_in_db(db, Stages, form.stage_id):
        new_stage_users_db = Stage_users(
            user_id=form.user_id,
            kpi=form.kpi,
            stage_id=form.stage_id,
        )
        save_in_db(db, new_stage_users_db)


def update_stage_users_s(form, db):
    if get_in_db(db, Stage_users, form.id) and get_in_db(db, Users, form.user_id) and get_in_db(db, Stages, form.stage_id):
        db.query(Stage_users).filter(Stage_users.id == form.id).update({
            Stage_users.user_id: form.user_id,
            Stage_users.kpi: form.kpi,
            Stage_users.stage_id: form.stage_id,
        })
        db.commit()


def delete_stage_user_r(id, db):
    if get_in_db(db, Stage_users, id):
        db.query(Stage_users).filter(Stage_users.id == id).delete()
        db.commit()
