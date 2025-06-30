import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from fastapi import FastAPI
from routes import admin, items, users, upload, orders

app = FastAPI()

app.include_router(admin.router)
app.include_router(items.router)
app.include_router(users.router)
app.include_router(upload.router)
app.include_router(orders.router)