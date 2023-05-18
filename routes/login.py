# from datetime import timedelta
#
# from fastapi import APIRouter, HTTPException, Depends, status
# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
#
# from db import database
# from models.users import Users
# from schemas.tokens import Token
# from utils.login import create_access_token
# session = Session()
#
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 111
#
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
#
#
# login_router = APIRouter(
#     prefix="/login",
#     tags=["Login operation"]
# )
#
#
#
# @login_router.post("/login", response_model=Token)
# async def login_for_access_token(db: Session = Depends(database), form_data: OAuth2PasswordRequestForm = Depends()):
#     user = db.query(Users).where(Users.username == form_data.username).first()
#     if user:
#         is_validate_password = pwd_context.verify(form_data.password, user.password_hash)
#     else:
#         is_validate_password = False
#
#     if not is_validate_password:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Login yoki parolda xatolik",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     db.query(Users).filter(Users.id == user.id).update({
#         Users.token: access_token
#     })
#     db.commit()
#     return {'id': user.id, "access_token": access_token, "token_type": "bearer", "role": user.role}