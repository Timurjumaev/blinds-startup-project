from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.phones import create_phone
from models.phones import Phones
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination
from models.users import Users
from utils.login import get_password_hash


def all_users(search, page, limit, status, branch_id,  db, thisuser):
    if thisuser.branch_id:
        users = db.query(Users).filter(Users.branch_id == thisuser.branch_id).options(joinedload(Users.phones),
                                                                                      joinedload(Users.files),
                                                                                      joinedload(Users.balansi))
    else:
        users = db.query(Users).options(joinedload(Users.phones),
                                        joinedload(Users.files))
    if branch_id:
        users = users.filter(Users.branch_id == branch_id)
    if search:
        search_formatted = "%{}%".format(search)
        users = users.filter(Users.name.like(search_formatted))
    if status:
        users = users.filter(Users.status == True)
    elif status is None:
        users = users
    else:
        users = users.filter(Users.status == False)
    users = users.order_by(Users.name.desc())
    return pagination(users, page, limit)


def one_user(db, user, ident):
    the_user = db.query(Users).filter(Users.branch_id == user.branch_id,
                                      Users.id == ident).options(joinedload(Users.phones),
                                                                 joinedload(Users.files)).first()
    if the_user is None:
        raise HTTPException(status_code=404)
    return the_user


def create_user_r(form, db, thisuser):
    if db.query(Users).filter(Users.username == form.username).first():
        raise HTTPException(status_code=400, detail="Username error")
    if form.role != "admin" and form.role != "worker" and form.role != "warehouseman" \
            and form.role != "crudadmin" and form.role != "crudoperator":
        raise HTTPException(status_code=400, detail="Role error!")
    password_hash = get_password_hash(form.password)
    new_user_db = Users(
        name=form.name,
        username=form.username,
        password=form.password,
        password_hash=password_hash,
        role=form.role,
        status=form.status,
        branch_id=thisuser.branch_id
    )
    save_in_db(db, new_user_db)
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, new_user_db.id, thisuser.id, db, 'user', thisuser.branch_id)


def create_branch_user_r(form, db, thisuser):
    if db.query(Users).filter(Users.username == form.username).first():
        raise HTTPException(status_code=400, detail="Username error")
    if form.role != "admin" and form.role != "worker" and form.role != "warehouseman":
        raise HTTPException(status_code=400, detail="Role error!")
    password_hash = get_password_hash(form.password)
    new_user_db = Users(
        name=form.name,
        username=form.username,
        password=form.password,
        password_hash=password_hash,
        role=form.role,
        status=form.status,
        branch_id=form.branch_id
    )
    save_in_db(db, new_user_db)
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, new_user_db.id, thisuser.id, db, 'user', form.branch_id)


def update_user_r(form, db, thisuser):
    the_one(db, Users, form.id, thisuser)
    if form.role != "admin" and form.role != "worker" and form.role != "warehouseman" \
            and form.role != "crudadmin" and form.role != "crudoperator":
        raise HTTPException(status_code=400, detail="Role error!")

    password_hash = get_password_hash(form.password)
    db.query(Users).filter(Users.id == form.id).update({
        Users.name: form.name,
        Users.username: form.username,
        Users.password: form.password,
        Users.password_hash: password_hash,
        Users.role: form.role,
        Users.status: form.status
    })
    db.commit()
    phones = db.query(Phones).filter(Phones.source == "user", Phones.source_id == form.id).all()
    for phone in phones:
        db.query(Phones).filter(Phones.id == phone.id).delete()
        db.commit()
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(comment, number, form.id, thisuser.id, db, 'user', thisuser.branch_id)




