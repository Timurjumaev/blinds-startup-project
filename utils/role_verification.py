from fastapi import HTTPException


def role_verification(user, function):
    allowed_functions_for_worker = []
    allowed_functions_for_warehouseman = []
    if user.role == "admin":
        return True
    elif user.role == "worker" and function in allowed_functions_for_worker:
        return True
    elif user.role == "warehouseman" and function in allowed_functions_for_warehouseman:
        return True
    raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')