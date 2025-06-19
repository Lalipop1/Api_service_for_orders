from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models.order import Order
from app.models.dish import Dish
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=List[OrderResponse])
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    return result.scalars().all()

@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dish).where(Dish.id.in_(order.dish_ids)))
    dishes = result.scalars().all()

    if len(dishes) != len(order.dish_ids):
        raise HTTPException(status_code=400, detail="One or more dishes not found")

    db_order = Order(customer_name=order.customer_name, dishes=dishes)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

@router.delete("/{order_id}")
async def cancel_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "в обработке":
        raise HTTPException(status_code=400, detail="Only orders in 'в обработке' can be cancelled")
    await db.delete(order)
    await db.commit()
    return {"message": "Order cancelled"}

@router.patch("/{order_id}/status")
async def update_status(order_id: int, update: OrderStatusUpdate, db: AsyncSession = Depends(get_db)):
    valid_transitions = {
        "в обработке": "готовится",
        "готовится": "доставляется",
        "доставляется": "завершен"
    }
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if valid_transitions.get(order.status) != update.status:
        raise HTTPException(status_code=400, detail=f"Invalid status transition from {order.status} to {update.status}")
    order.status = update.status
    await db.commit()
    return {"message": f"Order status updated to {update.status}"}
