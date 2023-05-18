from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.categories import categories_router
from routes.cells import cells_router
from routes.collactions import collactions_router
from routes.currencies import currencies_router
from routes.customers import customers_router
from routes.discounts import discounts_router
from routes.expenses import expenses_router
from routes.incomes import incomes_router
from routes.kassas import kassas_router
from routes.materials import materials_router
from routes.mechanisms import mechanisms_router
from routes.orders import orders_router
from routes.phones import phones_router
from routes.prices import prices_router
from routes.stage_users import stage_users_router
from routes.stages import stages_router
from routes.supplier_balances import supplier_balances_router
from routes.suppliers import suppliers_router
from routes.supplies import supplies_router
from routes.users import users_router
from routes.warehouse_materials import warehouse_materials_router
from routes.warehouses import warehouses_router
from utils.login import login_router

app = FastAPI()

app.include_router(users_router)
app.include_router(login_router)
app.include_router(categories_router)
app.include_router(collactions_router)
app.include_router(materials_router)
app.include_router(phones_router)
app.include_router(prices_router)
app.include_router(suppliers_router)
app.include_router(supplier_balances_router)
app.include_router(currencies_router)
app.include_router(warehouses_router)
app.include_router(supplies_router)
app.include_router(warehouse_materials_router)
app.include_router(mechanisms_router)
app.include_router(stages_router)
app.include_router(stage_users_router)
app.include_router(cells_router)
app.include_router(customers_router)
app.include_router(discounts_router)
app.include_router(orders_router)
app.include_router(kassas_router)
app.include_router(incomes_router)
app.include_router(expenses_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


