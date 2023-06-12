from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.loans import update_loan_n, all_loans
from models.loans import Loans
from utils.login import get_current_active_user
from utils.db_operations import get_in_db
from schemas.users import CreateUser
from schemas.loans import UpdateLoan
from db import database
import inspect
from utils.role_verification import role_verification


loans_router = APIRouter(
    prefix="/loans",
    tags=["Loans operation"]
)


@loans_router.get("/get_loans")
def get_loans(search: str = None, id: int = 0, page: int = 0, limit: int = 25, order_id: int = None,
              db: Session = Depends(database), current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Loans, id)
    return all_loans(search, page, limit, order_id, db)


@loans_router.put("/update_loan")
def update_loan(this_loan: UpdateLoan, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_loan_n(this_loan, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






