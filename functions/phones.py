from utils.db_operations import save_in_db
from utils.pagination import pagination
from models.phones import Phones


def all_phones(search, page, limit, db, thisuser):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Phones.number.like(search_formatted))
    else:
        search_filter = Phones.id > 0
    phones = db.query(Phones).filter(search_filter, Phones.branch_id == thisuser.branch_id).order_by(Phones.number.asc())
    return pagination(phones, page, limit)


def create_phone(comment, number, source_id, user_id, db, source, branch_id):
    new_phone_db = Phones(
        number=number,
        comment=comment,
        source=source,
        source_id=source_id,
        user_id=user_id,
        branch_id=branch_id
    )
    save_in_db(db, new_phone_db)

