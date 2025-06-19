from fastapi import FastAPI
from app.routers import dishes, orders

app = FastAPI(title="Restaurant API")

app.include_router(dishes.router)
app.include_router(orders.router)
